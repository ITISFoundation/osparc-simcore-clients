from typing import Callable, Iterator, TypeVar, Union

from osparc_client import (
    File,
    Job,
    LimitOffsetPageFile,
    LimitOffsetPageJob,
    LimitOffsetPageSolver,
    LimitOffsetPageStudy,
    Solver,
    Study,
)

Page = Union[
    LimitOffsetPageJob, LimitOffsetPageFile, LimitOffsetPageSolver, LimitOffsetPageStudy
]
T = TypeVar("T", Job, File, Solver, Study)


class PaginationIterator:
    """Class for wrapping paginated http methods as iterators"""

    def __init__(
        self,
        pagination_method: Callable[[int, int], Page],
        limit: int = 20,
        offset: int = 0,
    ):
        self._pagination_method: Callable[[int, int], Page] = pagination_method
        self._limit: int = limit
        self._offset: int = offset

    def __len__(self) -> int:
        """Number of elements which the iterator can produce

        Returns:
            int: The number of elements the iterator can produce
        """
        page: Page = self._pagination_method(self._limit, 0)
        assert isinstance(page.total, int)
        assert (
            page.total >= 0
        ), f"page.total={page.total} must be a nonnegative interger"
        return max(page.total - self._offset, 0)

    def __iter__(self) -> Iterator[T]:
        """Returns the iterator

        Yields:
            Iterator[T]: The returned iterator
        """
        if len(self) == 0:
            return
        while True:
            page: Page = self._pagination_method(self._limit, self._offset)
            assert page.items is not None
            assert isinstance(page.total, int)
            yield from page.items
            self._offset += len(page.items)
            if self._offset >= page.total:
                break
