---
applyTo: '.github/workflows/**'
---

# GitHub workflow instructions

Workflows live in [`.github/workflows`](../workflows/):
`build-and-test-python-client` builds the wheels and runs the unit tests across
the supported Python matrix, `publish-python-client` publishes to PyPI through
the `pypi` environment, and `publish-to-github-pages` builds `docs/` and deploys
the site.

## Referencing actions

- Reference a third-party action by full commit SHA plus a trailing comment with
  the release version it resolves to, e.g.
  `uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1`.
  Do not use a floating tag or a branch name.
- Resolve the tag to its commit with
  `gh api repos/<owner>/<repo>/commits/<tag> --jq .sha` and keep the SHA and its
  version comment in sync. Update one action per change so a bump is reviewable.
- Prefer first-party `actions/*` and `github/*` actions. Before adding a
  third-party action, read its source at the pinned commit: it runs with your
  token's permissions on the runner.

## Permissions and secrets

- Set `permissions:` at workflow level and narrow it further per job. The default
  token is broader than a job needs.
- Do not pass `GITHUB_TOKEN` to a step that runs code fetched from a pull
  request, and do not print or persist token material or `secrets.*` values in
  logs, artifacts, or job outputs.
- Do not check out a ref taken from an event payload
  (`github.event.client_payload.*`, a pull request head ref) in a workflow that
  can read write-scoped secrets. Resolve the ref from the trusted base branch
  instead.

## Python steps

- Use `uv` for the environment, as the `Makefile` targets do, rather than a bare
  `pip install` of unpinned packages. When a step needs a pip-only feature, run
  pip through uv (`uv run --no-project --with pip pip ...`) rather than
  installing pip into the environment.
- Keep the `python-version` matrix in sync with the versions the package
  supports. The floor is Python 3.9 until a release raises it, and raising it
  means changing the matrix in the same pull request. Adding a version to the
  matrix means the code must import and pass the unit tests on it.
- A workflow step that duplicates a `make` target should call the target, so the
  local and CI paths cannot drift.

## Diagnosing failures

- Read the failing step's log with `gh run view <run-id> --log-failed`, not the
  whole run. Compare against the same job on the base commit before concluding
  the change caused it.
- A job that fails only on one matrix entry is a version-specific issue; reproduce
  it locally with that interpreter before changing shared code.
