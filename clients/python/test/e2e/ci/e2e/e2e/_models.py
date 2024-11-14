import configparser
from pathlib import Path
from typing import Dict, Final, Set

import osparc
from packaging.version import InvalidVersion, Version
from pydantic import BaseModel, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Holds classes for passing data around between scripts.


class ServerSettings(BaseSettings):
    """Holds data about server configuration"""

    host: str
    key: SecretStr
    secret: SecretStr
    email: str
    password: SecretStr

    model_config = SettingsConfigDict(env_prefix="osparc_api_")

    def __hash__(self):
        return hash(
            self.host + self.key.get_secret_value() + self.secret.get_secret_value()
        )

    def __eq__(self, other):
        return (
            self.host == other.host
            and self.key.get_secret_value() == other.key.get_secret_value()
            and self.secret.get_secret_value() == other.secret.get_secret_value()
        )


def is_empty(v):
    return v is None or v == ""


_CLIENT_VERSION_IDS: Final[Set[str]] = {"latest_release", "latest_master"}


class ClientSettings(BaseSettings):
    """Holds data about client configuration.
    This data should uniquely determine how to install client
    """

    version: str

    @field_validator("version", mode="after")
    @classmethod
    def _validate_client(cls, v):
        if v not in _CLIENT_VERSION_IDS:
            try:
                version = Version(v)
                assert version == Version(osparc.__version__)
            except InvalidVersion as e:
                raise ValueError(f"Received invalid semantic version: {v}") from e
            except AssertionError as e:
                raise ValueError(f"{v=} != {osparc.__version__=}") from e
        return v

    @property
    def ref(self) -> str:
        """Returns the reference for this client in the compatibility table"""
        return f"{osparc.__version__}"

    @property
    def compatibility_ref(self) -> str:
        """Returns the reference for this client in the compatibility table"""
        return "master" if self.version == "latest_master" else "production"


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
            # WARNING: this is a temporary solution until we learn how to customize
            # the serialization used in model_dump
            config[field_name] = {
                name: value.get_secret_value()
                if isinstance(value, SecretStr)
                else value
                for name, value in model.model_dump(exclude_none=True).items()
            }

        with open(pth, "w") as f:
            config.write(f)
