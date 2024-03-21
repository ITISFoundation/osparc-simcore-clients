import httpx
import osparc
import pytest
from osparc._http_client import AsyncHttpClient


@pytest.fixture
def fake_retry_state():
    def _(r: httpx.Response):
        class Exc:
            response = r

        class Outcome:
            def exception(self):
                return Exc()

        class FakeRetryCallState:
            outcome = Outcome()

        return FakeRetryCallState()

    yield _


def test_retry_strategy(cfg: osparc.Configuration, fake_retry_state):
    async_client = AsyncHttpClient(
        configuration=cfg,
        request_type="get",
        url="79ae41cc-0d89-4714-ac9d-c23ee1b110ce",
    )
    assert (
        async_client._wait_callback(
            fake_retry_state(
                httpx.Response(
                    status_code=503,
                    headers={"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"},
                )
            )
        )
        < 0
    )
    assert (
        async_client._wait_callback(
            fake_retry_state(
                httpx.Response(
                    status_code=503,
                    headers={"Retry-After": "15"},
                )
            )
        )
        == 15
    )
