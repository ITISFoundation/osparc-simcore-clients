from typing import List, Optional

import httpx
from osparc_client import OnePageSolverPort, SolverPort
from osparc_client import SolversApi as _SolversApi

from . import ApiClient


class SolversApi(_SolversApi):
    """Class for interacting with solvers"""

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
        )
        return page.items
