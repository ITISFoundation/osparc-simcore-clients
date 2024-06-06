from typing import Any, List, Optional

import httpx
from osparc_client import OnePageSolverPort, SolverPort
from osparc_client import SolversApi as _SolversApi

from . import ApiClient
from ._models import ParentProjectInfo
from ._utils import PaginationGenerator, dev_feature, dev_features_enabled


class SolversApi(_SolversApi):
    """Class for interacting with solvers"""

    _dev_features = [
        "get_jobs_page",
    ]

    def __getattribute__(self, name: str) -> Any:
        if (name in SolversApi._dev_features) and (not dev_features_enabled()):
            raise NotImplementedError(f"SolversApi.{name} is still under development")
        return super().__getattribute__(name)

    def __init__(self, api_client: Optional[ApiClient] = None):
        """Construct object

        Args:
            api_client (ApiClient, optinal): osparc.ApiClient object
        """
        self._super: _SolversApi = super()
        self._super.__init__(api_client)
        user: Optional[str] = self.api_client.configuration.username
        passwd: Optional[str] = self.api_client.configuration.password
        self._auth: Optional[httpx.BasicAuth] = (
            httpx.BasicAuth(username=user, password=passwd)
            if (user is not None and passwd is not None)
            else None
        )

    def list_solver_ports(self, solver_key: str, version: str) -> List[SolverPort]:
        page: OnePageSolverPort = self._super.list_solver_ports(
            solver_key=solver_key, version=version
        )  # type: ignore
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

        def pagination_method():
            return super(SolversApi, self).get_jobs_page(
                solver_key=solver_key, version=version, limit=20, offset=0
            )

        return PaginationGenerator(
            first_page_callback=pagination_method,
            api_client=self.api_client,
            base_url=self.api_client.configuration.host,
            auth=self._auth,
        )

    def create_job(self, solver_key, version, job_inputs, **kwargs):
        kwargs = {**kwargs, **ParentProjectInfo().model_dump(exclude_none=True)}
        return super().create_job(solver_key, version, job_inputs, **kwargs)
