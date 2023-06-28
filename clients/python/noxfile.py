import nox
from pathlib import Path


py_dir = Path(__file__).parent.resolve()
nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True


@nox.session(python=["3.6", "3.7", "3.8", "3.9"])
def test(session):

    options = session.posargs
    if "-k" in options or "-x" in options:
        options.append("--no-cov")

    dist_dir = Path(__file__).parent / 'artifacts' / 'dist'
    if not dist_dir.is_dir():
        raise RuntimeError(f'Could not find {dist_dir}. Did you forget to generate the client wheels?')

    dir_content = dist_dir.glob('*')
    osparc_wheels = list(dist_dir.glob('*osparc-*.whl'))
    if len(osparc_wheels) != 1:
        raise RuntimeError(f'Could not find osparc_wheel. It is not in {dist_dir}: {dir_content}.')

    session.install(osparc_wheels[0], "--find-links", dist_dir)
    session.run("pytest", "-v", f"--ignore={py_dir/'artifacts/client'}",*options)
