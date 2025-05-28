# Wraps osparc_client.api.solvers_api

from typing import List, Optional

import httpx
from osparc_client.api.solvers_api import SolversApi as _SolversApi
from .models import (
    JobInputs,
    OnePageSolverPort,
    SolverPort,
    Job,
    JobOutputs,
    JobMetadata,
    JobMetadataUpdate,
)
from osparc_client import JobInputs as _JobInputs
from osparc_client import JobMetadataUpdate as _JobMetadataUpdate

from ._api_client import ApiClient
from ._settings import ParentProjectInfo
from ._utils import (
    _DEFAULT_PAGINATION_LIMIT,
    _DEFAULT_PAGINATION_OFFSET,
    PaginationIterable,
)
import warnings
from tempfile import NamedTemporaryFile
from pathlib import Path
from pydantic import validate_call
from pydantic import StrictStr


class SolversApi(_SolversApi):
    """Class for interacting with solvers"""

    _dev_features = [
        "get_jobs_page",
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

    def list_solver_ports(
        self, solver_key: str, version: str, **kwargs
    ) -> List[SolverPort]:
        page: OnePageSolverPort = super().list_solver_ports(
            solver_key=solver_key, version=version, **kwargs
        )
        return page.items if page.items else []

    def iter_jobs(self, solver_key: str, version: str, **kwargs) -> PaginationIterable:
        """Returns an iterator through which one can iterate over
        all Jobs submitted to the solver

        Args:
            solver_key (str): The solver key
            version (str): The solver version
            limit (int, optional): the limit of a single page
            offset (int, optional): the offset of the first element to return

        Returns:
            PaginationGenerator: A generator whose elements are the Jobs submitted
            to the solver and the total number of jobs the iterator can yield
            (its "length")
        """

        def _pagination_method():
            return super(SolversApi, self).get_jobs_page(
                solver_key=solver_key,
                version=version,
                limit=_DEFAULT_PAGINATION_LIMIT,
                offset=_DEFAULT_PAGINATION_OFFSET,
                **kwargs,
            )

        return PaginationIterable(
            first_page_callback=_pagination_method,
            api_client=self.api_client,
            base_url=self.api_client.configuration.host,
            auth=self._auth,
        )

    def jobs(self, solver_key: str, version: str, **kwargs) -> PaginationIterable:
        warnings.warn(
            "The 'jobs' method is deprecated and will be removed in a future version. "
            "Please use 'iter_jobs' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.iter_jobs(solver_key, version, **kwargs)

    @validate_call
    def create_job(
        self, solver_key: str, version: str, job_inputs: JobInputs, **kwargs
    ) -> Job:
        _job_inputs = _JobInputs.from_json(job_inputs.model_dump_json())
        assert _job_inputs is not None
        kwargs = {**kwargs, **ParentProjectInfo().model_dump(exclude_none=True)}
        return super().create_solver_job(solver_key, version, _job_inputs, **kwargs)

    def get_job_output_logfile(
        self,
        solver_key: str,
        version: str,
        job_id: StrictStr,
        **kwargs,
    ):
        data = super().get_job_output_logfile(
            solver_key=solver_key, version=version, job_id=job_id, **kwargs
        )
        with NamedTemporaryFile(delete=False) as tmp_file:
            log_file = Path(tmp_file.name)
            log_file.write_bytes(data)
            return log_file

    def get_job_outputs(
        self,
        solver_key: str,
        version: str,
        job_id: StrictStr,
        **kwargs,
    ) -> JobOutputs:
        _osparc_client_outputs = super().get_job_outputs(
            solver_key=solver_key, version=version, job_id=job_id, **kwargs
        )
        return JobOutputs.model_validate_json(_osparc_client_outputs.to_json())

    def get_job_custom_metadata(self, *args, **kwargs) -> JobMetadata:
        metadata = super().get_job_custom_metadata(*args, **kwargs)
        return JobMetadata.model_validate_json(metadata.to_json())

    @validate_call
    def replace_job_custom_metadata(
        self,
        solver_key: str,
        version: str,
        job_id: str,
        job_metadata_update: JobMetadataUpdate,
    ) -> JobMetadata:
        _job_metadata_update = _JobMetadataUpdate.from_json(
            job_metadata_update.model_dump_json()
        )
        assert _job_metadata_update is not None
        _job_custom_metadata = super().replace_job_custom_metadata(
            solver_key, version, job_id, _job_metadata_update
        )
        return JobMetadata.model_validate_json(_job_custom_metadata.to_json())
