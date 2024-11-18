from contextlib import suppress
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Optional,
    Set,
    Literal,
    AsyncGenerator,
)

import httpx
import tenacity
from osparc_client import Configuration

_RETRY_AFTER_STATUS_CODES: Set[int] = {429, 503}


class AsyncHttpClient:
    """Async http client context manager"""

    def __init__(
        self,
        *,
        configuration: Configuration,
        method: Optional[str] = None,
        url: Optional[str] = None,
        body: Optional[Dict] = None,
        **httpx_async_client_kwargs,
    ):
        self.configuration = configuration
        self._client = httpx.AsyncClient(**httpx_async_client_kwargs)
        self._callback = getattr(self._client, method) if method else None
        self._url = url
        self._body = body
        if self._callback is not None:
            assert self._url is not None  # nosec
            assert self._body is not None  # nosec

    async def __aenter__(self) -> "AsyncHttpClient":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if exc_value is None:
            await self._client.aclose()
        else:  # exception raised: need to handle
            if self._callback is not None:
                try:
                    async for attempt in tenacity.AsyncRetrying(
                        reraise=True,
                        wait=tenacity.wait_fixed(1),
                        stop=tenacity.stop_after_delay(10),
                        retry=tenacity.retry_if_exception_type(httpx.RequestError),
                    ):
                        with attempt:
                            response = await self._callback(
                                self._url, json={} if self._body is None else self._body
                            )
                            response.raise_for_status()
                except httpx.HTTPError as err:
                    await self._client.aclose()
                    raise err from exc_value
            await self._client.aclose()
            raise exc_value

    async def _request(
        self, method: Callable[[Any], Awaitable[httpx.Response]], *args, **kwargs
    ) -> httpx.Response:
        n_attempts = self.configuration.retries.total
        assert isinstance(n_attempts, int)

        @tenacity.retry(
            reraise=True,
            wait=self._wait_callback,
            stop=tenacity.stop_after_attempt(n_attempts),
            retry=tenacity.retry_if_exception_type(httpx.HTTPStatusError),
        )
        async def _():
            response: httpx.Response = await method(*args, **kwargs)
            if response.status_code in self.configuration.retries.status_forcelist:
                response.raise_for_status()
            return response

        return await _()

    async def _stream(
        self, method: Literal["GET"], url: str, *args, **kwargs
    ) -> AsyncGenerator[httpx.Response, None]:
        n_attempts = self.configuration.retries.total
        assert isinstance(n_attempts, int)

        @tenacity.retry(
            reraise=True,
            wait=self._wait_callback,
            stop=tenacity.stop_after_attempt(n_attempts),
            retry=tenacity.retry_if_exception_type(httpx.HTTPStatusError),
        )
        async def _() -> AsyncGenerator[httpx.Response, None]:
            async with self._client.stream(
                method=method, url=url, *args, **kwargs
            ) as response:
                if response.status_code in self.configuration.retries.status_forcelist:
                    response.raise_for_status()
                yield response

        return _()

    async def put(self, *args, **kwargs) -> httpx.Response:
        return await self._request(self._client.put, *args, **kwargs)

    async def post(self, *args, **kwargs) -> httpx.Response:
        return await self._request(self._client.post, *args, **kwargs)

    async def delete(self, *args, **kwargs) -> httpx.Response:
        return await self._request(self._client.delete, *args, **kwargs)

    async def patch(self, *args, **kwargs) -> httpx.Response:
        return await self._request(self._client.patch, *args, **kwargs)

    async def get(self, *args, **kwargs) -> httpx.Response:
        return await self._request(self._client.get, *args, **kwargs)

    async def stream(
        self, method: Literal["GET"], url: str, *args, **kwargs
    ) -> AsyncGenerator[httpx.Response, None]:
        return await self._stream(method=method, url=url, *args, **kwargs)

    def _wait_callback(self, retry_state: tenacity.RetryCallState) -> int:
        assert retry_state.outcome is not None
        if retry_state.outcome and retry_state.outcome.exception():
            response: httpx.Response = retry_state.outcome.exception().response
            if response.status_code in _RETRY_AFTER_STATUS_CODES:
                retry_after = response.headers.get("Retry-After")
                if retry_after is not None:
                    with suppress(ValueError, TypeError):
                        next_try = parsedate_to_datetime(retry_after)
                        return int(
                            (
                                next_try - datetime.now(tz=next_try.tzinfo)
                            ).total_seconds()
                        )
                    with suppress(ValueError):
                        return int(retry_after)
        # https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#utilities
        return self.configuration.retries.backoff_factor * (
            2**retry_state.attempt_number
        )
