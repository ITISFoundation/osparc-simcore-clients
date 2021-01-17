from logging import currentframe
import pytest
from dotenv import dotenv_values
from pathlib import Path
from typing import Dict
import sys


current_dir = Path( sys.argv[0] if __name__ == "__main__" else __file__  ).parent.resolve()

@pytest.fixture(scope="session")
def root_repo_dir() -> Path:
    repo_dir = current_dir.parent
    assert any( repo_dir.glob(".git") )
    return repo_dir


@pytest.fixture(scope="session")
def project_env_dict(root_repo_dir: Path) -> Dict:
    env_file = root_repo_dir / ".env"
    assert env_file.exists()
    environ = dotenv_values(env_file, verbose=True, interpolate=True)
    return environ


@pytest.fixture
def project_environ_patched(project_env_dict, monkeypatch) -> Dict:
    for key, value in project_env_dict.items():
        monkeypatch.setenv(key, value)
    return project_env_dict