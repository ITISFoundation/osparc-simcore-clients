---
applyTo: '**/*.py'
---

# Python instructions

The Python client is two packages: `osparc_client`, which is generated from
[`api/openapi.json`](../../api/openapi.json) and is not committed, and `osparc`,
the hand-written wrapper in
[`clients/python/src/osparc`](../../clients/python/src/osparc). Tests are in
[`clients/python/test`](../../clients/python/test). The supported interpreter
range is the matrix in
[`build-python-client.yml`](../workflows/build-python-client.yml), with a floor
of Python 3.9.

## Generated code

- Never edit generated code by hand. Regenerate with `make python-client` in
  [`clients/python/Makefile`](../../clients/python/Makefile), or change the
  generator or its templates in
  [openapi-generator](https://github.com/ITISFoundation/openapi-generator). If
  the behavior must come from the wrapper instead, change `src/osparc`.
- The API surface `osparc` exposes over the generated one lives in
  `src/osparc/api.py`, `models.py`, and `exceptions.py`. Keep them explicit
  `from ._x import X as X` re-exports in alphabetical order and add no logic
  there.
- When `api/openapi.json` changes, regenerate the client and commit the
  specification change and the resulting code in the same pull request.

## Compatibility and typing

- Write code for the oldest interpreter in the CI matrix. Do not rewrite existing
  code solely to modernize syntax.
- Fully annotate parameters and return types of all functions and methods,
  including private helpers. Annotate class attributes and non-obvious values.
- Declare module-level constants as `NAME: Final[T] = value` with an explicit
  type, including private ones and constants in test modules.

## Documentation

- Prefer clear names, types, and small functions over comments.
- Document only public or non-obvious behavior: contracts, side effects,
  invariants, concurrency constraints. Use `Raises:` only for exceptions callers
  must handle.
- Rationale for a function, fixture, or test belongs in its docstring, not in a
  `# NOTE:` comment.
- Do not narrate bug history or incident stories in inline comments; a single
  factual sentence about the constraint is enough.

## Imports and logging

- Import at module scope. Import locally only to avoid a verified cycle or defer
  an optional or expensive dependency. Explain the reason briefly.
- Use relative imports inside the `osparc` package and absolute imports for
  `osparc_client` and third-party packages.
- Use f-strings, except in logging, which defers formatting:
  `logger.info("Retrieved %d studies for %s", count, api_key_id)`.
- Use logging, not `print()`, in the package. `print()` belongs in scripts under
  [`scripts/`](../../scripts/) and in generator templates, and needs a comment
  where its use looks out of place.

## Retries

- Use `tenacity` for retries in this package. Do not hand-write retry loops with
  `sleep`.
- Bound every retry with `stop_after_attempt` or `stop_after_delay`. Use
  `wait_exponential` or `wait_random_exponential` for remote calls. Retry only
  specific exceptions with `retry_if_exception_type`. Log retries with
  `before_sleep_log`.
- Transport-level retries of the generated client go through the `urllib3.Retry`
  instance built in
  [`_configuration.py`](../../clients/python/src/osparc/_configuration.py).
  Keep its allowed methods and status codes explicit; do not widen them as a
  side effect of other changes.
- Do not retry a request that is not idempotent unless the endpoint documents
  that it is safe to repeat.

## Pydantic, serialization, and configuration

- Use only Pydantic v2 APIs, such as `model_dump`, `model_validate`,
  `model_copy`, and `ConfigDict`.
- Keep credentials in `SecretStr` or `SecretBytes`. Unwrap them only where the
  code needs the raw value. Never log them.
- Environment-backed settings live in
  [`_settings.py`](../../clients/python/src/osparc/_settings.py) as
  `pydantic-settings` models. Add new configuration there, with a default, a
  validator, and a documented environment variable name.
- Keep request and response payloads on the generated models; do not introduce a
  parallel model hierarchy for fields the specification already defines.

## Async code

- Do not block the event loop in `async` functions with synchronous file,
  process, or network calls.
- Bound every await on a remote call with the client's timeout configuration.
  A call without a deadline must have a reason in a comment.

## Suppressions

- Use `assert` only for dev-time invariants and type narrowing, never as part of
  a logic workflow. In package code under `src/`, mark every `assert` with
  `# nosec` to acknowledge bandit's assert plugin; test assertions need none.
- Use `# type: ignore[code]` only for a narrow typing limitation, with the most
  specific code and a reason when non-obvious.
- Use `# noqa: <RULE>` only for a specific rule, never `# noqa: E999`-style
  blanket suppression of a file.
