# AGENTS.md

Entry point for AI agents working in this repository. It indexes the instruction
files and skills that hold the repository's conventions; read the ones whose
`applyTo` pattern matches the files you are editing. For human-oriented setup and
workflows, see the [Development notes](./README.md#development-notes) and the
per-client [README](./clients/python/README.md).

## Instruction files

In [`.github/instructions`](./.github/instructions/). Apply every file whose
`applyTo` pattern matches; where two rules conflict, the file-type-specific rule
wins.

| File                                     | Applies to                                          | Covers                                                            |
| ---------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------- |
| [`general`](./.github/instructions/general.instructions.md)             | `**`                      | Change discipline, secrets, tests and validation, comments, git workflow, pull request descriptions |
| [`python`](./.github/instructions/python.instructions.md)               | `**/*.py`                 | Generated versus hand-written client code, Python floor, typing, imports and logging, retries, pydantic settings, suppressions |
| [`python-tests`](./.github/instructions/python-tests.instructions.md)   | `clients/python/test/**/*.py`, `**/test_*.py`, `**/conftest.py` | `pytest` structure, parametrization, fixtures, `autouse`, test file naming, how to run each test level |
| [`github-workflows`](./.github/instructions/github-workflows.instructions.md) | `.github/workflows/**`   | Pinning actions to a commit SHA, token permissions and secrets, Python matrix steps, reading failed logs |

## Skills

In [`.github/skills`](./.github/skills/).

| Skill                                       | Use it for                                                  |
| ------------------------------------------- | ----------------------------------------------------------- |
| [`unit-test`](./.github/skills/unit-test/SKILL.md)                 | Running the Python client's unit tests             |
| [`e2e-test`](./.github/skills/e2e-test/SKILL.md)                   | Running the end-to-end tests against a deployment  |
| [`debug-e2e-tests`](./.github/skills/debug-e2e-tests/SKILL.md)     | Investigating a failing end-to-end test, including server-side logs |
| [`unslop`](./.github/skills/unslop/SKILL.md)                       | Rewriting pull request text, commit messages, docs and comments into plain factual prose |

## Pull requests

Descriptions follow
[`.github/PULL_REQUEST_TEMPLATE.md`](./.github/PULL_REQUEST_TEMPLATE.md): fill
every section, `n/a` where one does not apply, and run
[`unslop`](./.github/skills/unslop/SKILL.md) on the text before posting. Pull
requests are squash-merged, so the title carries the gitmoji prefix listed in the
template.
