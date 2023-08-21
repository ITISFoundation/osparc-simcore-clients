import configparser
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import ParseResult, urlparse

from _utils import _PYTEST_INI
from packaging.version import Version
from pydantic import AnyUrl, BaseModel, field_validator, model_validator

# Holds classes for passing data around between scripts.


class ServerConfig(BaseModel):
    """Holds data about server configuration"""

    OSPARC_API_HOST: AnyUrl
    OSPARC_API_KEY: str
    OSPARC_API_SECRET: str

    @property
    def url(self) -> ParseResult:
        return urlparse(f"{self.OSPARC_API_HOST}")

    @property
    def key(self) -> str:
        return self.OSPARC_API_KEY

    @property
    def secret(self) -> str:
        return self.OSPARC_API_SECRET


def is_empty(v):
    return v is None or v == ""


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
            except Exception:
                raise ValueError(f"Did not receive valid version: {v}")
        return v

    @model_validator(mode="after")
    def check_consistency(self) -> "ClientConfig":
        msg: str = (
            f"Recieved OSPARC_CLIENT_VERSION={self.OSPARC_CLIENT_VERSION}, "
            f"OSPARC_CLIENT_REPO={self.OSPARC_CLIENT_REPO}"
            "and OSPARC_CLIENT_BRANCH={self.OSPARC_CLIENT_BRANCH}. "
            "Either a version or a repo, branch pair must be specified. Not both."
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


class PytestConfig(BaseModel):
    """Holds the pytest configuration
    N.B. paths are relative to clients/python/test/e2e
    """

    env: str
    required_plugins: str
    addopts: str


class Artifacts(BaseModel):
    artifact_dir: Path
    result_data_frame: Path
    log_dir: Path


class PytestIniFile(BaseModel):
    """Model for validating the .ini file"""

    pytest: PytestConfig
    client: ClientConfig
    server: ServerConfig
    artifacts: Artifacts

    @classmethod
    def read(cls) -> "PytestIniFile":
        """Read the pytest.ini file"""
        if not _PYTEST_INI.is_file():
            raise ValueError(
                f"_PYTEST_INI: {_PYTEST_INI} must point to a pytest.ini file"
            )
        with open(_PYTEST_INI, "r") as f:
            obj = configparser.ConfigParser()
            obj.read(f)
            config_dict: Dict = {s: dict(obj.items(s)) for s in obj.sections()}
        return PytestIniFile(**config_dict)

    def generate(self, pth: Path = _PYTEST_INI) -> None:
        """Generate the pytest.ini file"""
        pth.unlink(missing_ok=True)
        pth.parent.mkdir(exist_ok=True)
        config: configparser.ConfigParser = configparser.ConfigParser()
        for field_name in self.__fields__:
            model: BaseModel = getattr(self, field_name)
            config[field_name] = model.model_dump(exclude_none=True)
        with open(pth, "w") as f:
            config.write(f)
