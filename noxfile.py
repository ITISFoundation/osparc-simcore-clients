import nox

nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True

source_files = ("osparc", "test", "setup.py", "noxfile.py")
lint_requirements = ("flake8", "black", "isort")
docs_requirements = ("mkdocs", "mkdocs-material", "mkautodoc>=0.1.0")


@nox.session(python=["3.6", "3.7", "3.8"])
def test(session):
    session.install("--upgrade", "pytest", "pytest-asyncio", "pytest-cov", "pytest-randomly")
    session.install("-e", ".")

    options = session.posargs
    if "-k" in options or "-x" in options:
        options.append("--no-cov")

    session.run("pytest", "-v", *options)


@nox.session
def docs(session):
    session.install("--upgrade", *docs_requirements)
    session.install("-e", ".")

    args = session.posargs if session.posargs else ["build"]
    session.run("mkdocs", *args)


@nox.session(reuse_venv=True)
def watch(session):
    session.install("--upgrade", *docs_requirements)
    session.install("-e", ".")

    session.run("mkdocs", "serve")
