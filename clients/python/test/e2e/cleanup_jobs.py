"""Deletes every job of every solver release on the deployment in the environment.

An interrupted run leaves submitted jobs behind on the server, which then hold resources on
a shared deployment. The deployment and credentials come from OSPARC_API_HOST,
OSPARC_API_KEY and OSPARC_API_SECRET, the same variables the tests read. Run it after the
suite; in CI, from a step that also runs when the tests fail.
"""

import argparse
import logging
import os
from datetime import timedelta

import osparc
import tenacity
from urllib3.exceptions import HTTPError as Urllib3HttpError

_logger = logging.getLogger(__name__)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--retry-minutes",
        type=int,
        default=None,
        help="retry the whole sweep for this many minutes when the server answers with "
        "an API error. Without it, a single attempt is made.",
    )
    return parser.parse_args()


def _delete_all_jobs(api_client: osparc.ApiClient) -> int:
    solvers_api = osparc.SolversApi(api_client=api_client)
    deleted = 0
    releases = solvers_api.list_solvers_releases()
    _logger.info("Scanning %d solver releases", len(releases))
    for solver in releases:
        for job in solvers_api.iter_jobs(solver.id, solver.version):
            solvers_api.delete_job(solver.id, solver.version, job.id)
            deleted += 1
    return deleted


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = _parse_args()

    host = os.environ.get("OSPARC_API_HOST")
    username = os.environ.get("OSPARC_API_KEY")
    password = os.environ.get("OSPARC_API_SECRET")
    if not (host and username and password):
        _logger.error(
            "OSPARC_API_HOST, OSPARC_API_KEY and OSPARC_API_SECRET must be set"
        )
        return 1

    configuration = osparc.Configuration(
        host=host, username=username, password=password
    )
    stop = (
        tenacity.stop_after_delay(timedelta(minutes=args.retry_minutes))
        if args.retry_minutes
        else tenacity.stop_after_attempt(1)
    )
    try:
        with osparc.ApiClient(configuration=configuration) as api_client:
            for attempt in tenacity.Retrying(
                retry=tenacity.retry_if_exception_type(
                    (osparc.ApiException, Urllib3HttpError)
                ),
                stop=stop,
                wait=tenacity.wait_fixed(10),
                reraise=True,
            ):
                with attempt:
                    deleted = _delete_all_jobs(api_client)
    except Exception as exc:
        _logger.error("Failed to clean up jobs on %s: %s", host, exc)
        return 1

    _logger.info("Deleted %d jobs on %s", deleted, host)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
