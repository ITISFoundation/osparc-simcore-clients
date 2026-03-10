---
name: unit-test
description: Run the Python unit tests for the osparc client
---

To run the Python unit tests, execute the following command from the `clients/python` directory:

```bash
cd clients/python
VIRTUAL_ENV=../../.venv uv run pytest test/test_osparc
```
