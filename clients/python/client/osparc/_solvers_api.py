from typing import Any, Iterator

from osparc_client import SolversApi as _SolversApi

from . import ApiClient, Job


class SolversApi:
    """Class for interacting with solvers"""

    def __init__(self, api_client: ApiClient):
        """Construct object

        Args:
            api_client (ApiClient): osparc.ApiClient object
        """
        self._api_client: ApiClient = api_client
        self._solvers_api: _SolversApi = _SolversApi(api_client)

    def get_jobs(self, solver_key: str, version: str, **kwargs) -> Iterator[Job]:
        """Returns an iterator through which one can iterate over all Jobs submitted to the solver

        Args:
            solver_key (str): The solver key
            version (str): The solver version

        Yields:
            Iterator[Job]: An iterator whose elements are the Jobs submitted to the solver
        """
        limit: int = 20
        offset: int = 0

    def __getattr__(self, __name: str) -> Any:
        return getattr(self._solvers_api, __name)
