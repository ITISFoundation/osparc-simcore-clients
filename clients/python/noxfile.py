import nox
from pathlib import Path


py_dir = Path(__file__).parent.resolve()
nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True

source_files = ("osparc", "test", "setup.py", "noxfile.py")

@nox.session(python=["3.6", "3.7", "3.8", "3.9"])
def test(session):
    session.install("-r", "artifacts/client/test-requirements.txt")
    session.install("-e", "artifacts/client/")

    options = session.posargs
    if "-k" in options or "-x" in options:
        options.append("--no-cov")

    session.run("pytest", "-v", f"--ignore={py_dir/'artifacts/client'}",*options)
