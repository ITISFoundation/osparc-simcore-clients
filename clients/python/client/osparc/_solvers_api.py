from typing import Optional

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

    def get_jobs_page(self, solver_key: str, version: str) -> None:
        """Method only for internal use"""
        raise NotImplementedError("This method is only for internal use")

    def get_jobs(
        self, solver_key: str, version: str, limit: int = 20, offset: int = 0
    ) -> PaginationGenerator:
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

        def pagination_method(limit, offset):
            return super(SolversApi, self).get_jobs_page(
                solver_key=solver_key, version=version, limit=limit, offset=offset
            )

        return PaginationGenerator(pagination_method, limit, offset)
