from typing import Any, Iterator, List

from osparc_client import SolversApi as _SolversApi

from . import ApiClient, Job
from ._utils import _pagination_to_iterator


class SolversApi:
    """Class for interacting with solvers"""

    _wrapped_methods: List[str] = ["get_jobs"]

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
        pagination_method = lambda limit, offset: self._solvers_api.get_jobs_page(
            solver_key=solver_key, version=version, limit=limit, offset=offset
        )
        return _pagination_to_iterator(pagination_method=pagination_method)

    def __getattr__(self, name: str) -> Any:
        if name in self._wrapped_methods:
            return getattr(self, name)
        else:
            return getattr(self._solvers_api, name)
