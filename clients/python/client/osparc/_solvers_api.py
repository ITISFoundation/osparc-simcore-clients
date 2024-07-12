from typing import Any, List, Optional

import httpx
from osparc_client import JobInputs, OnePageSolverPort, SolverPort
from osparc_client import SolversApi as _SolversApi

from ._api_client import ApiClient
from ._models import ParentProjectInfo
from ._utils import (
    _DEFAULT_PAGINATION_LIMIT,
    _DEFAULT_PAGINATION_OFFSET,
    PaginationGenerator,
    dev_feature,
    dev_features_enabled,
)


class SolversApi(_SolversApi):
    """Class for interacting with solvers"""

    _dev_features = [
        "get_jobs_page",
    ]

    def __getattr__(self, name: str) -> Any:
        if (name in SolversApi._dev_features) and (not dev_features_enabled()):
            raise NotImplementedError(f"SolversApi.{name} is still under development")
        return super().__getattribute__(name)

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

    @dev_feature
    def jobs(self, solver_key: str, version: str) -> PaginationGenerator:
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
            )

        return PaginationGenerator(
            first_page_callback=_pagination_method,
            api_client=self.api_client,
            base_url=self.api_client.configuration.host,
            auth=self._auth,
        )

    def create_job(
        self, solver_key: str, version: str, job_inputs: JobInputs, **kwargs
    ):
        kwargs = {**kwargs, **ParentProjectInfo().model_dump(exclude_none=True)}
        return super().create_job(solver_key, version, job_inputs, **kwargs)
