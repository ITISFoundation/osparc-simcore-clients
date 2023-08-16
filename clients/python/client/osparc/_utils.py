import asyncio
from pathlib import Path
from typing import AsyncGenerator, Callable, Generator, TypeVar, Union

from osparc_client import (
    File,
    Job,
    PageFile,
    PageJob,
    PageSolver,
    PageStudy,
    Solver,
    Study,
)

Page = Union[PageJob, PageFile, PageSolver, PageStudy]
T = TypeVar("T", Job, File, Solver, Study)


class PaginationGenerator:
    """Class for wrapping paginated http methods as generators"""

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

    def __iter__(self) -> Generator[T, None, None]:
        """Returns the generator

        Yields:
            Generator[T,None,None]: The returned generator
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


async def _file_chunk_generator(
    file: Path, chunk_size: int
) -> AsyncGenerator[tuple[bytes, int], None]:
    if not file.is_file():
        raise RuntimeError(f"{file} must be a file")
    if chunk_size <= 0:
        raise RuntimeError(f"chunk_size={chunk_size} must be a positive int")
    bytes_read: int = 0
    file_size: int = file.stat().st_size
    while bytes_read < file_size:
        with open(file, "rb") as f:
            f.seek(bytes_read)
            nbytes = (
                chunk_size
                if (bytes_read + chunk_size <= file_size)
                else (file_size - bytes_read)
            )
            assert nbytes > 0
            chunk = await asyncio.get_event_loop().run_in_executor(None, f.read, nbytes)
            yield chunk, nbytes
            bytes_read += nbytes


S = TypeVar("S")


async def _fcn_to_coro(callback: Callable[..., S], *args) -> S:
    """Get an awaitable from a callback."""
    result = await asyncio.get_event_loop().run_in_executor(None, callback, args)
    return result
