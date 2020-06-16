import nox

nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True


docs_requirements = ("mkdocs", "mkdocs-material", "mkautodoc>=0.1.0")


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
