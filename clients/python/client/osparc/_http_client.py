from typing import Any, Awaitable, Callable, Optional

import httpx
import tenacity
from osparc_client import Configuration


class AsyncHttpClient:
    """Async http client context manager"""

    def __init__(
        self,
        *,
        configuration: Configuration,
        request_type: Optional[str] = None,
        url: Optional[str] = None,
        **httpx_async_client_kwargs
    ):
        self.configuration = configuration
        self._client = httpx.AsyncClient(**httpx_async_client_kwargs)
        self._callback = getattr(self._client, request_type) if request_type else None
        self._url = url

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
                            response = await self._callback(self._url)
                            response.raise_for_status()
                except Exception as err:
                    await self._client.aclose()
                    raise err from exc_value
            await self._client.aclose()
            raise exc_value

    async def _request(
        self, method: Callable[[Any], Awaitable[httpx.Response]], *args, **kwargs
    ) -> httpx.Response:
        async for attempt in tenacity.AsyncRetrying(
            reraise=True,
            wait=tenacity.wait_exponential(
                multiplier=self.configuration.retries.backoff_factor
            ),
            stop=tenacity.stop_after_attempt(
                self.configuration.retries.total
                if isinstance(self.configuration.retries.total, int)
                else 4
            ),
            retry=tenacity.retry_if_exception_type(httpx.HTTPStatusError),
        ):
            with attempt:
                response: httpx.Response = await method(*args, **kwargs)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    if (
                        exc.response.status_code
                        in self.configuration.retries.status_forcelist
                    ):
                        raise exc
                return response

    async def put(self, *args, **kwargs) -> httpx.Response:
        return await self._request(self._client.put, *args, **kwargs)

    async def post(self, *args, **kwargs) -> httpx.Response:
        return await self._request(self._client.post, *args, **kwargs)

    async def delete(self, *args, **kwargs) -> httpx.Response:
        return await self._request(self._client.delete, *args, **kwargs)

    async def patch(self, *args, **kwargs) -> httpx.Response:
        return await self._request(self._client.patch, *args, **kwargs)
