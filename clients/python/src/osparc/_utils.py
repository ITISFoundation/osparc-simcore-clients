import asyncio
import hashlib
from pathlib import Path
from typing import (
    AsyncGenerator,
    Callable,
    Optional,
    TypeVar,
    Union,
    NamedTuple,
    Generator,
)
from collections.abc import Iterable, Sized
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
from .exceptions import RequestError

_KB = 1024  # in bytes
_MB = _KB * 1024  # in bytes
_GB = _MB * 1024  # in bytes

_DEFAULT_PAGINATION_LIMIT: int = 20
_DEFAULT_PAGINATION_OFFSET: int = 0

DEFAULT_TIMEOUT_SECONDS: int = 30 * 60

Page = Union[PageJob, PageFile, PageStudy]
T = TypeVar("T", Job, File, Solver, Study)


class PaginationIterable(Iterable, Sized):
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
        self._next_page_url: Optional[str] = None
        self._client: httpx.Client = httpx.Client(
            auth=auth, base_url=base_url, follow_redirects=True
        )

    def __del__(self):
        self._client.close()

    def __len__(self) -> int:
        """Number of elements which the iterator can produce"""
        page: Page = self._first_page_callback()
        assert isinstance(page.total, int)
        return page.total

    def __iter__(self) -> Generator[T, None, None]:
        """Returns the generator"""
        if len(self) == 0:
            return
        page: Page = self._first_page_callback()
        while True:
            assert page.items is not None
            assert isinstance(page.total, int)
            yield from page.items
            if page.links.next is None:
                return
            response: httpx.Response = self._client.get(page.links.next)
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise RequestError(f"{e}") from e
            page = self._api_client._ApiClient__deserialize(response.json(), type(page))


class Chunk(NamedTuple):
    data: bytes
    nbytes: int
    is_last_chunk: bool


async def file_chunk_generator(
    file: Path, chunk_size: int
) -> AsyncGenerator[Chunk, None]:
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
            yield Chunk(
                data=chunk, nbytes=nbytes, is_last_chunk=(bytes_read == file_size)
            )


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
