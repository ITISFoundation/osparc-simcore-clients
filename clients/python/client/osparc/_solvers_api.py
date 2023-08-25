from typing import Optional

import httpx
from osparc_client import SolversApi as _SolversApi

from . import ApiClient
from ._utils import PaginationGenerator


class SolversApi(_SolversApi):
    """Class for interacting with solvers"""

    def __init__(self, api_client: Optional[ApiClient] = None):
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

    def get_jobs_page(self, solver_key: str, version: str) -> None:
        """Method only for internal use"""
        raise NotImplementedError("This method is only for internal use")

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
            pagination_method,
            base_url=self.api_client.configuration.host,
            auth=self._auth,
        )
