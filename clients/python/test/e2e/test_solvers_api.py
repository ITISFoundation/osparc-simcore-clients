# pylint: disable=protected-access
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import json

import osparc
import tenacity
from _utils import skip_if_osparc_version
from httpx import AsyncClient
from packaging.version import Version
from uuid import UUID
import pytest
from contextlib import contextmanager
from typing import Callable, Iterator, Set
from tenacity import Retrying

DEFAULT_TIMEOUT_SECONDS = 15 * 60  # 15 min


@pytest.fixture
def create_sleeper_jobs(
    api_client: osparc.ApiClient,
    sleeper: osparc.Solver,
) -> Callable[[int], Iterator[Set[UUID | str]]]:
    @contextmanager
    def sleeper_jobs(n_jobs: int = 1) -> Iterator[Set[UUID | str]]:
        job_ids = set()
        solvers_api = osparc.SolversApi(api_client=api_client)
        try:
            for _ in range(n_jobs):
                job = solvers_api.create_job(
                    sleeper.id, sleeper.version, osparc.JobInputs({"input1": 1.0})
                )
                assert isinstance(job, osparc.Job)
                print(job.to_str())
                job_ids.add(job.id)
            yield job_ids
        finally:
            for job_id in job_ids:
                for attempt in Retrying(
                    reraise=True,
                    wait=tenacity.wait_fixed(2),
                    stop=tenacity.stop_after_delay(60),
                ):
                    with attempt:
                        solvers_api.stop_job(sleeper.id, sleeper.version, job_id)
                        solvers_api.delete_job(sleeper.id, sleeper.version, job_id)

    return sleeper_jobs


@skip_if_osparc_version(at_least=Version("0.8.3.post0.dev20"))
def test_jobs(
    api_client: osparc.ApiClient,
    create_sleeper_jobs: Callable[[int], Iterator[Set[UUID | str]]],
    sleeper: osparc.Solver,
):
    """Test the jobs method

    Args:
        configuration (osparc.Configuration): The Configuration
    """
    n_jobs: int = 3
    solvers_api = osparc.SolversApi(api_client=api_client)
    # initial iterator
    init_iter = solvers_api.iter_jobs(sleeper.id, sleeper.version)
    n_init_iter: int = len(init_iter)
    assert n_init_iter >= 0

    # create n_jobs jobs
    with create_sleeper_jobs(n_jobs):
        tmp_iter = solvers_api.iter_jobs(sleeper.id, sleeper.version)
        solvers_api.iter_jobs(sleeper.id, sleeper.version)
        final_iter = solvers_api.iter_jobs(sleeper.id, sleeper.version)
        assert len(final_iter) > 0, "No jobs were available"
        assert n_init_iter + n_jobs == len(
            final_iter
        ), "An incorrect number of jobs was recorded"

        for ii, elm in enumerate(tmp_iter):
            assert isinstance(elm, osparc.Job)
            if ii > 100:
                break


@skip_if_osparc_version(at_least=Version("0.6.5"))
async def test_logstreaming(
    api_client: osparc.ApiClient,
    sleeper: osparc.Solver,
    create_sleeper_jobs: Callable[[int], Iterator[Set[UUID]]],
    async_client: AsyncClient,
):
    """Test log streaming"""
    solvers_api: osparc.SolversApi = osparc.SolversApi(api_client)
    with create_sleeper_jobs() as jobs:
        job_id = next(iter(jobs))

        solvers_api.start_job(sleeper.id, sleeper.version, job_id)

        nloglines: int = 0
        url = f"/v0/solvers/{sleeper.id}/releases/{sleeper.version}/jobs/{job_id}/logstream"
        print(f"starting logstreaming from {url}...")

        async with async_client.stream(
            "GET",
            url,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        ) as response:
            print(response.headers)
            async for line in response.aiter_lines():
                log = json.loads(line)
                log_job_id = log.get("job_id")
                assert log_job_id
                assert log_job_id == (
                    f"{job_id}" if isinstance(job_id, UUID) else job_id
                )  # keep test backwards compatible
                nloglines += 1
                print("\n".join(log.get("messages")))
                await response.aclose()
                break

        assert nloglines > 0, f"Could not stream log for {sleeper.id=}, \
            {sleeper.version=} and {job_id=}"  # type: ignore
