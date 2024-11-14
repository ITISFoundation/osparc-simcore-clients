# Wraps osparc_client.api.studies_api

import asyncio
import logging
from pathlib import Path
from tempfile import mkdtemp
from typing import Optional

import httpx
from .models import JobInputs, JobLogsMap, PageStudy
from osparc_client.api.studies_api import StudiesApi as _StudiesApi
from tqdm.asyncio import tqdm_asyncio

from ._api_client import ApiClient
from ._http_client import AsyncHttpClient
from ._settings import ParentProjectInfo
from ._utils import (
    _DEFAULT_PAGINATION_LIMIT,
    _DEFAULT_PAGINATION_OFFSET,
    PaginationGenerator,
)
import warnings

_logger = logging.getLogger(__name__)


class StudiesApi(_StudiesApi):
    """Class for interacting with solvers"""

    _dev_features = [
        "clone_study",
        "create_study_job",
        "delete_study_job",
        "get_study",
        "get_study_job",
        "inspect_study_job",
        "list_studies",
        "list_study_jobs",
        "list_study_ports",
        "replace_study_job_custom_metadata",
        "start_study_job",
        "stop_study_job",
    ]

    def __init__(self, api_client: ApiClient):
        """Construct object

        Args:
            api_client (ApiClient, optinal): osparc.ApiClient object
        """
        super().__init__(api_client)
        user: Optional[str] = self.api_client.configuration.username
        passwd: Optional[str] = self.api_client.configuration.password
        self._auth: Optional[httpx.BasicAuth] = (
            httpx.BasicAuth(username=user, password=passwd)
            if (user is not None and passwd is not None)
            else None
        )

    def create_study_job(self, study_id: str, job_inputs: JobInputs, **kwargs):
        kwargs = {**kwargs, **ParentProjectInfo().model_dump(exclude_none=True)}
        return super().create_study_job(study_id, job_inputs, **kwargs)

    def clone_study(self, study_id: str, **kwargs):
        kwargs = {**kwargs, **ParentProjectInfo().model_dump(exclude_none=True)}
        return super().clone_study(study_id, **kwargs)

    def iter_studies(self, **kwargs) -> PaginationGenerator:
        def _pagination_method():
            page_study = self.list_studies(
                limit=_DEFAULT_PAGINATION_LIMIT,
                offset=_DEFAULT_PAGINATION_OFFSET,
                **kwargs,
            )
            assert isinstance(page_study, PageStudy)  # nosec
            return page_study

        return PaginationGenerator(
            first_page_callback=_pagination_method,
            api_client=self.api_client,
            base_url=self.api_client.configuration.host,
            auth=self._auth,
        )

    def studies(self, **kwargs) -> PaginationGenerator:
        warnings.warn(
            "The 'studies' method is deprecated and will be removed in a future version. "
            "Please use 'iter_studies' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.iter_studies(**kwargs)

    def get_study_job_output_logfiles(self, study_id: str, job_id: str) -> Path:
        return asyncio.run(
            self.get_study_job_output_logfiles_async(study_id=study_id, job_id=job_id)
        )

    async def get_study_job_output_logfiles_async(
        self, study_id: str, job_id: str, download_dir: Optional[Path] = None
    ) -> Path:
        """Download study logs. The log from each node will
        appear as a file with the node's name in the directory"""
        if download_dir is not None and not download_dir.is_dir():
            raise RuntimeError(f"{download_dir=} must be a valid directory")
        logs_map = super().get_study_job_output_logfile(study_id, job_id)
        assert isinstance(logs_map, JobLogsMap)  # nosec
        log_links = logs_map.log_links
        assert log_links  # nosec

        folder = download_dir or Path(mkdtemp()).resolve()
        assert folder.is_dir()  # nosec
        async with AsyncHttpClient(
            configuration=self.api_client.configuration
        ) as client:

            async def _download(unique_node_name: str, download_link: str) -> None:
                response = await client.get(download_link)
                response.raise_for_status()
                file = folder / unique_node_name
                ct = 1
                while file.exists():
                    file = file.with_stem(f"{file.stem}({ct})")
                    ct += 1
                file.touch()
                for chunk in response.iter_bytes():
                    file.write_bytes(chunk)

            tasks = [
                asyncio.create_task(_download(link.node_name, link.download_link))
                for link in log_links
            ]
            _logger.debug(
                "Downloading log files for study_id=%s and job_id=%s...",
                study_id,
                job_id,
            )
            await tqdm_asyncio.gather(
                *tasks, disable=(not _logger.isEnabledFor(logging.DEBUG))
            )

        return folder
