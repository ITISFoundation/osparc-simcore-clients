---
name: e2e-test
description: Run the Python end-to-end tests for the osparc client
---

To run the Python end-to-end tests, execute the following command in the terminal:

```bash
uv run pytest clients/python/test/e2e
```

The tests run against a real deployment, so `OSPARC_API_HOST`, `OSPARC_API_KEY` and
`OSPARC_API_SECRET` must be exported first. If they are not set, ask which deployment to test
against and where its credentials are; do not guess a host. Add `--junitxml=<path>.xml` when a
machine-readable report is wanted. `test/e2e/pytest.ini` holds the flags constant to this suite.

Note that you must use the python virtual environment located at `../../.venv` to ensure that the tests run with the correct dependencies.


If pytest is not installed into the virtual environment, you can install the test dependencies by running

```bash
source .venv/bin/activate
cd clients/python
make install-dev
cd -
```
