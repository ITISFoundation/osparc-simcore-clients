import configparser
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import ParseResult, urlparse

from _utils import _PYTEST_INI
from packaging.version import Version
from pydantic import BaseModel, field_validator, model_validator

# Holds classes for passing data around between scripts.


class ServerConfig(BaseModel):
    """Holds data about server configuration"""

    osparc_api_host: str
    osparc_api_key: str
    osparc_api_secret: str

    @property
    def url(self) -> ParseResult:
        return urlparse(f"{self.osparc_api_host}")

    @property
    def key(self) -> str:
        return self.osparc_api_key

    @property
    def secret(self) -> str:
        return self.osparc_api_secret


def is_empty(v):
    return v is None or v == ""


class ClientConfig(BaseModel):
    """Holds data about client configuration.
    This data should uniquely determine how to install client
    """

    osparc_client_version: Optional[str] = None
    osparc_client_repo: Optional[str] = None
    osparc_client_branch: Optional[str] = None
    osparc_dev_features: bool = False
    osparc_client_workflow: Optional[str] = None
    osparc_client_runid: Optional[str] = None

    @field_validator("osparc_client_version")
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
            f"Recieved osparc_client_version={self.osparc_client_version}, "
            f"osparc_client_repo={self.osparc_client_repo}"
            "and osparc_client_branch={self.osparc_client_branch}. "
            "Either a version or a repo, branch pair must be specified. Not both."
        )
        # check at least one is empty
        if not (
            is_empty(self.osparc_client_version)
            or (
                is_empty(self.osparc_client_repo)
                and is_empty(self.osparc_client_branch)
            )
        ):
            raise ValueError(msg)
        # check not both empty
        if is_empty(self.osparc_client_version) and (
            is_empty(self.osparc_client_repo) and is_empty(self.osparc_client_branch)
        ):
            raise ValueError(msg)
        if is_empty(self.osparc_client_version):
            if (
                is_empty(self.osparc_client_repo)
                or is_empty(self.osparc_client_branch)
                or is_empty(self.osparc_client_workflow)
                or is_empty(self.osparc_client_runid)
            ):
                raise ValueError(msg)
        return self

    @property
    def version(self) -> Optional[str]:
        return self.osparc_client_version

    @property
    def repo(self) -> Optional[str]:
        return self.osparc_client_repo

    @property
    def branch(self) -> Optional[str]:
        return self.osparc_client_branch

    @property
    def workflow(self) -> Optional[str]:
        return self.osparc_client_workflow

    @property
    def runid(self) -> Optional[str]:
        return self.osparc_client_runid

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
    def read(cls, pth: Path = _PYTEST_INI) -> "PytestIniFile":
        """Read the pytest.ini file"""
        if not pth.is_file():
            raise ValueError(f"pth: {pth} must point to a pytest.ini file")
        obj = configparser.ConfigParser()
        obj.read(pth)
        config: Dict = {s: dict(obj.items(s)) for s in obj.sections()}
        return PytestIniFile(**config)

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
