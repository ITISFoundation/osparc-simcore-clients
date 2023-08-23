import asyncio
from pathlib import Path
from typing import AsyncGenerator, Callable, Generator, Optional, Tuple, TypeVar, Union

import httpx
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
        first_page_callback: Callable[[], Page],
        base_url: str,
        auth: Optional[httpx.BasicAuth],
    ):
        self._first_page_callback: Callable[[], Page] = first_page_callback
        self._next_page_url: Optional[str] = None
        self._client: httpx.Client = httpx.Client(auth=auth, base_url=base_url)

    def __del__(self):
        self._client.close()

    def __len__(self) -> int:
        """Number of elements which the iterator can produce

        Returns:
            int: The number of elements the iterator can produce
        """
        page: Page = self._first_page_callback()
        assert isinstance(page.total, int)
        return page.total

    def __iter__(self) -> Generator[T, None, None]:
        """Returns the generator

        Yields:
            Generator[T,None,None]: The returned generator
        """
        if len(self) == 0:
            return
        page: Page = self._first_page_callback()
        while True:
            assert page.items is not None
            assert isinstance(page.total, int)
            yield from page.items
            if page.links.last is None:
                break
            response: httpx.Response = self._client.get(page.links.next)
            page = type(page)(**response.json())


async def _file_chunk_generator(
    file: Path, chunk_size: int
) -> AsyncGenerator[Tuple[bytes, int], None]:
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
    """Get a coroutine from a callback."""
    result = await asyncio.get_event_loop().run_in_executor(None, callback, *args)
    return result
