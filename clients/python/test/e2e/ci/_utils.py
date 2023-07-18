from enum import IntEnum
from pathlib import Path
from typing import Optional
from urllib.parse import ParseResult, urlparse

import pytest
from packaging.version import Version
from pydantic import BaseModel, field_validator, model_validator


# classed for handling errors -------------------------------------------------------------------------
class E2eScriptFailure(UserWarning):
    """Simply used to indicate a CI script failure"""

    pass


class E2eExitCodes(IntEnum):
    """Exitcodes
    Note these should not clash with pytest exitcodes: https://docs.pytest.org/en/7.1.x/reference/exit-codes.html
    """

    CI_SCRIPT_FAILURE = 100
    INVALID_CLIENT_VS_SERVER = 101
    INVALID_JSON_DATA = 102


assert (
    set(e.value for e in E2eExitCodes).intersection(
        set(e.value for e in pytest.ExitCode)
    )
    == set()
)

# Data classes ----------------------------------------------------------------------------------------


class ServerConfig(BaseModel):
    """Holds data about server configuration"""

    OSPARC_API_HOST: str
    OSPARC_API_KEY: str
    OSPARC_API_SECRET: str

    @field_validator("OSPARC_API_HOST")
    def check_url(cls, v):
        try:
            _ = urlparse(v)
        except:
            raise ValueError("Could not parse 'OSPARC_API_HOST'. Received {v}.")
        return v

    @property
    def url(self) -> ParseResult:
        return urlparse(self.OSPARC_API_HOST)

    @property
    def key(self) -> str:
        return self.OSPARC_API_KEY

    @property
    def secret(self) -> str:
        return self.OSPARC_API_SECRET


is_empty = lambda v: v is None or v == ""


class ClientConfig(BaseModel):
    """Holds data about client configuration.
    This data should uniquely determine how to install client
    """

    OSPARC_CLIENT_VERSION: Optional[str] = None
    OSPARC_CLIENT_REPO: Optional[str] = None
    OSPARC_CLIENT_BRANCH: Optional[str] = None
    OSPARC_CLIENT_WORKFLOW: Optional[str] = None
    OSPARC_CLIENT_RUNID: Optional[str] = None

    @field_validator("OSPARC_CLIENT_VERSION")
    def validate_client(cls, v):
        if (not is_empty(v)) and (not v == "latest"):
            try:
                _ = Version(v)
            except:
                raise ValueError(f"Did not receive valid version: {v}")
        return v

    @model_validator(mode="after")
    def check_consistency(self) -> "ClientConfig":
        msg: str = (
            f"Recieved OSPARC_CLIENT_VERSION={self.OSPARC_CLIENT_VERSION}, OSPARC_CLIENT_REPO={self.OSPARC_CLIENT_REPO}"
            "and OSPARC_CLIENT_BRANCH={self.OSPARC_CLIENT_BRANCH}. Either a version or a repo, branch pair must be specified. Not both."
        )
        # check at least one is empty
        if not (
            is_empty(self.OSPARC_CLIENT_VERSION)
            or (
                is_empty(self.OSPARC_CLIENT_REPO)
                and is_empty(self.OSPARC_CLIENT_BRANCH)
            )
        ):
            raise ValueError(msg)
        # check not both empty
        if is_empty(self.OSPARC_CLIENT_VERSION) and (
            is_empty(self.OSPARC_CLIENT_REPO) and is_empty(self.OSPARC_CLIENT_BRANCH)
        ):
            raise ValueError(msg)
        if is_empty(self.OSPARC_CLIENT_VERSION):
            if (
                is_empty(self.OSPARC_CLIENT_REPO)
                or is_empty(self.OSPARC_CLIENT_BRANCH)
                or is_empty(self.OSPARC_CLIENT_WORKFLOW)
                or is_empty(self.OSPARC_CLIENT_RUNID)
            ):
                raise ValueError(msg)
        return self

    @property
    def version(self) -> Optional[str]:
        return self.OSPARC_CLIENT_VERSION

    @property
    def repo(self) -> Optional[str]:
        return self.OSPARC_CLIENT_REPO

    @property
    def branch(self) -> Optional[str]:
        return self.OSPARC_CLIENT_BRANCH

    @property
    def workflow(self) -> Optional[str]:
        return self.OSPARC_CLIENT_WORKFLOW

    @property
    def runid(self) -> Optional[str]:
        return self.OSPARC_CLIENT_RUNID

    @property
    def compatibility_ref(self) -> str:
        """Returns the reference for this client in the compatibility table"""
        if not is_empty(self.version):
            return "production"
        else:
            assert isinstance(self.branch, str)
            return self.branch

    @property
    def client_ref(self) -> str:
        """Returns a short hand reference for this client"""
        if not is_empty(self.version):
            assert isinstance(self.version, str)
            return self.version
        else:
            assert isinstance(self.branch, str)
            return self.branch


# Paths ---------------------------------------------------------------------------------------------

_E2E_DIR: Path = Path(__file__).parent.parent.resolve()
_CI_DIR: Path = (_E2E_DIR / "ci").resolve()
_PYPROJECT_TOML: Path = (_E2E_DIR / "pyproject.toml").resolve()
_ARTIFACTS_DIR: Path = (_E2E_DIR / ".." / ".." / "artifacts" / "e2e").resolve()
_COMPATIBILITY_JSON: Path = (
    _E2E_DIR / "data" / "server_client_compatibility.json"
).resolve()

assert _COMPATIBILITY_JSON.is_file()
