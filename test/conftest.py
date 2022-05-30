import pytest

from pathlib import Path
import sys


current_dir = Path(sys.argv[0] if __name__ == "__main__" else __file__).parent.resolve()


@pytest.fixture(scope="session")
def root_repo_dir() -> Path:
    repo_dir = current_dir.parent
    assert any(repo_dir.glob(".git"))
    return repo_dir
