import configparser
from pathlib import Path
from typing import Dict

import osparc
from packaging.version import InvalidVersion, Version
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Holds classes for passing data around between scripts.


class ServerSettings(BaseSettings):
    """Holds data about server configuration"""

    host: str
    key: str
    secret: str

    model_config = SettingsConfigDict(env_prefix="osparc_api_")

    def __hash__(self):
        return hash(self.host + self.key + self.secret)

    def __eq__(self, other):
        return (
            self.host == other.host
            and self.key == other.key
            and self.secret == other.secret
        )


def is_empty(v):
    return v is None or v == ""


class ClientSettings(BaseSettings):
    """Holds data about client configuration.
    This data should uniquely determine how to install client
    """

    version: str
    dev_features: bool = False

    @field_validator("version", mode="after")
    def validate_client(cls, v):
        if v not in {"latest_release", "latest_master"}:
            try:
                version = Version(v)
                assert version == Version(osparc.__version__)
            except InvalidVersion:
                raise ValueError(f"Received invalid semantic version: {v}")
            except AssertionError:
                raise ValueError(f"{v=} != {osparc.__version__=}")
        return v

    @property
    def ref(self) -> str:
        """Returns the reference for this client in the compatibility table"""
        if self.dev_features:
            return f"{osparc.__version__}+dev_features"
        else:
            return f"{osparc.__version__}-dev_features"

    @property
    def compatibility_ref(self) -> str:
        """Returns the reference for this client in the compatibility table"""
        if self.version == "latest_master":
            if self.dev_features:
                return "master+dev_features"
            else:
                return "master-dev_features"
        else:
            return "production"


class PytestConfig(BaseModel):
    """Holds the pytest configuration
    N.B. paths are relative to clients/python/test/e2e
    """

    env: str
    required_plugins: str
    addopts: str
    asyncio_mode: str


class Artifacts(BaseModel):
    artifact_dir: Path
    result_data_frame: Path
    log_dir: Path


class PytestIniFile(BaseModel):
    """Model for validating the .ini file"""

    pytest: PytestConfig
    client: ClientSettings
    server: ServerSettings
    artifacts: Artifacts

    @classmethod
    def create_from_file(cls, pth: Path = Path() / "pytest.ini") -> "PytestIniFile":
        """Read the pytest.ini file"""
        if not pth.is_file():
            raise ValueError(f"pth: {pth} must point to a pytest.ini file")
        obj = configparser.ConfigParser()
        obj.read(pth)
        config: Dict = {s: dict(obj.items(s)) for s in obj.sections()}
        return PytestIniFile(**config)

    def write_to_file(self, pth: Path = Path() / "pytest.ini") -> None:
        """Generate the pytest.ini file"""
        pth.unlink(missing_ok=True)
        pth.parent.mkdir(exist_ok=True)
        config: configparser.ConfigParser = configparser.ConfigParser()
        for field_name in self.model_fields:
            model: BaseModel = getattr(self, field_name)
            config[field_name] = model.model_dump(exclude_none=True)
        with open(pth, "w") as f:
            config.write(f)
