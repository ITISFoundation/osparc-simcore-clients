---
name: e2e-test
description: Run the Python end-to-end tests for the osparc client
---

To run the Python end-to-end tests, execute the following command in the terminal:

```bash
uv run pytest clients/python/test/e2e
```

Note that you must use the python virtual environment located at `../../.venv` to ensure that the tests run with the correct dependencies.


If pytest is not installed into the virtual environment, you can install the test dependencies by running

```bash
source .venv/bin/activate
cd clients/python
make install-dev
cd -
```
