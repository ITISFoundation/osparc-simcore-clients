---
applyTo: 'clients/python/test/**/*.py,**/test_*.py,**/conftest.py'
---

# Python test instructions

Unit tests live in
[`clients/python/test/test_osparc`](../../clients/python/test/test_osparc),
end-to-end tests against a real deployment in
[`clients/python/test/e2e`](../../clients/python/test/e2e), and the documentation
snippet tests in
[`tests_docs.py`](../../clients/python/test/tests_docs.py). Fixtures are shared
through the `conftest.py` files at each of those levels.

## Test structure

- Use `pytest` with module-level `test_*` functions. Do not use `class Test...`
  containers solely to group tests.
- Name tests after behavior and scenario, e.g.
  `test_list_studies_filters_by_user_id()`.
- Do not annotate return types of `test_*` functions or methods. Their
  parameters still require annotations.
- Test externally observable behavior, not private implementation details.

## Parametrization

- Remove repetition only when it improves readability. Keep the scenario under
  test clear.
- Use `pytest.mark.parametrize` for cases with the same flow and give them
  stable, descriptive IDs. Keep separate tests when setup, intent, or failure
  diagnosis differ.

## Fixtures

- Reuse existing fixtures from the `conftest.py` files and the test module
  before adding new ones. Before writing a test, search for an existing fixture
  or helper for each collaborator it needs (client instance, configuration, user
  or study fixtures, server stubs). Search every `conftest.py` up the test tree
  and the fixtures defined in sibling test modules. Do not copy fixtures or fakes
  from an earlier test, including one you wrote yourself, without repeating this
  search.
- When a sibling test module defines a fixture you need, move it to the nearest
  `conftest.py` and use it from both modules. Do not duplicate it.
- Prefer `mock.create_autospec(Client, instance=True)` over hand-written fakes
  such as `SimpleNamespace`, so that calls are checked against the real
  signature. Do not patch private functions of the code under test when its
  collaborators can be replaced through their public API.
- Extract repeated, meaningful setup into a named fixture or factory. Keep small
  setup inline when a fixture would hide it.
- Name a fixture that returns a callable which creates or performs something (a
  callback-style fixture) with a `create_` prefix, e.g. `create_study`, so call
  sites read as actions. Do not name it after the created object alone.
- Fixtures must not leak mutable state, files, network resources, environment
  variables, time patches, or monkeypatches into other tests. End-to-end
  fixtures must delete what they created on the deployment, or the test must be
  named so the leftover is identifiable.

## `autouse=True` fixtures

- Do not add `autouse=True` fixtures in `conftest.py`.
- Use `autouse=True` only for a fixture defined and used in the same test
  module. Add a short comment above it explaining why explicit injection is
  impractical.

## Shared test data types

- Do not import dataclasses, `TypedDict`s, or other test-support types from
  another test module or from `conftest.py`. Pytest's import behavior makes this
  fragile.
- Put types shared across end-to-end modules in
  [`e2e/_utils.py`](../../clients/python/test/e2e/_utils.py), and keep types that
  one module needs in that module.

## File and directory names

- Test filenames must be unique across the test tree. Avoid generic names such
  as `test_list.py`.
- When splitting a module, keep the full original prefix in each filename, and
  name the directory after the original filename without `test_`.
- Split test modules over 1,000 lines by behavior or scenario. Move shared
  fixtures to the nearest `conftest.py`. Do not split if it would duplicate setup
  or obscure relationships.

## Running tests

- Unit tests: follow the [`unit-test`](../skills/unit-test/SKILL.md) procedure.
  Start with the single file or test that covers the change and broaden to the
  whole `test_osparc` tree when the change crosses module, serialization, or
  HTTP-client boundaries.
- End-to-end tests: follow the [`e2e-test`](../skills/e2e-test/SKILL.md)
  procedure. They require a reachable deployment and its credentials in the
  environment; they are not a substitute for a unit test. When one fails against
  a shared deployment, use
  [`debug-e2e-tests`](../skills/debug-e2e-tests/SKILL.md) to read the server-side
  logs before changing the test.
