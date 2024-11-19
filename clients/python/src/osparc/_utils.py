import asyncio
import hashlib
from pathlib import Path
from typing import AsyncGenerator, Callable, Optional, Tuple, TypeVar, Union, cast, List
from collections.abc import Iterator
import httpx
from osparc_client import (
    ApiClient,
    File,
    Job,
    PageFile,
    PageJob,
    PageStudy,
    Solver,
    Study,
)
import aiofiles

_KB = 1024  # in bytes
_MB = _KB * 1024  # in bytes
_GB = _MB * 1024  # in bytes

_DEFAULT_PAGINATION_LIMIT: int = 20
_DEFAULT_PAGINATION_OFFSET: int = 0

DEFAULT_TIMEOUT_SECONDS: int = 30 * 60

Page = Union[PageJob, PageFile, PageStudy]
T = TypeVar("T", Job, File, Solver, Study)


class PaginationIterator(Iterator):
    """Class for wrapping paginated http methods as iterables. It supports three simple operations:
    - for elm in pagination_iterable
    - elm = next(pagination_iterable)
    - len(pagination_iterable)"""

    def __init__(
        self,
        first_page_callback: Callable[[], Page],
        api_client: ApiClient,
        base_url: str,
        auth: Optional[httpx.BasicAuth],
    ):
        self._first_page_callback: Callable[[], Page] = first_page_callback
        self._api_client: ApiClient = api_client
        self._client: httpx.Client = httpx.Client(
            auth=auth, base_url=base_url, follow_redirects=True
        )
        self._page: Optional[Page] = None
        self._items_iterator: Optional[Iterator] = None

    def __del__(self):
        self._client.close()

    def __next__(self):
        if self._page is None:
            self._page = self._first_page_callback()
            self._items_iterator = iter(cast(List, self._page.items))
        assert self._items_iterator is not None  # nosec
        try:
            return next(self._items_iterator)
        except StopIteration as exc:
            next_page_url = self._page.links.next
            if next_page_url is None:
                self._page = None
                self._items_iterator = None
                raise StopIteration from exc
            response = self._client.get(next_page_url)
            self._page = self._api_client._ApiClient__deserialize(
                response.json(), type(self._page)
            )
            assert self._page is not None  # nosec
            self._items_iterator = iter(cast(List, self._page.items))
            return next(self._items_iterator)

    def __len__(self) -> int:
        """Number of elements which the iterator can produce"""
        if self._page is not None:
            return cast(int, self._page.total)
        self._page = self._first_page_callback()
        return cast(int, self._page.total)


async def file_chunk_generator(
    file: Path, chunk_size: int
) -> AsyncGenerator[Tuple[bytes, int, bool], None]:
    if not file.is_file():
        raise RuntimeError(f"{file} must be a file")
    if chunk_size <= 0:
        raise RuntimeError(f"chunk_size={chunk_size} must be a positive int")
    bytes_read: int = 0
    file_size: int = file.stat().st_size
    while bytes_read < file_size:
        async with aiofiles.open(file, "rb") as f:
            await f.seek(bytes_read)
            nbytes = (
                chunk_size
                if (bytes_read + chunk_size <= file_size)
                else (file_size - bytes_read)
            )
            assert nbytes > 0
            chunk = await f.read(nbytes)
            bytes_read += nbytes
            yield chunk, nbytes, (bytes_read == file_size)


S = TypeVar("S")


async def _fcn_to_coro(callback: Callable[..., S], *args) -> S:
    """Get a coroutine from a callback."""
    result = await asyncio.get_event_loop().run_in_executor(None, callback, *args)
    return result


async def compute_sha256(file: Path) -> str:
    assert file.is_file()
    sha256 = hashlib.sha256()
    async with aiofiles.open(file, "rb") as f:
        while True:
            data = await f.read(100 * _KB)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()
