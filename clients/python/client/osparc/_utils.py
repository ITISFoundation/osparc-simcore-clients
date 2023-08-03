from typing import Any, Callable, Iterator, TypeVar, Union

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


def _pagination_to_iterator(
    pagination_method: Callable[[int, int], Page], limit: int = 20
) -> Iterator[T]:
    """Returns an iterator given a pagination entrypoint

    Args:
        pagination_method (Callable[[int, int], Page]): A lambda which takes as first input the limit and as second input the offset of the page
        limit (int, optional): Limit of the page. Defaults to 20.

    Raises:
        StopIteration: Raised when one has iterated through all elements in the iterator

    Yields:
        Iterator[T]: The returned iterator
    """
    offset: int = 0
    item_count: int = 0
    while True:
        page: Page = pagination_method(limit, offset)
        assert page.items is not None
        assert isinstance(page.total, int)
        for item in page.items:
            item_count += 1
            yield item
        offset += limit
        if item_count >= page.total:
            raise StopIteration