---
applyTo: '**'
---

# General repository conventions

This repository contains the clients for the o²S²PARC public API. The Python
client lives in [`clients/python`](../../clients/python/), its generated sources
in [`clients/python/src/osparc`](../../clients/python/src/osparc), and the API
specification they are generated from in
[`api/openapi.json`](../../api/openapi.json).

Use the Python version in the CI matrix of
[`build-python-client.yml`](../workflows/build-python-client.yml). The floor is
Python 3.9: do not use syntax or standard-library features unavailable in that
version. Apply all instruction files whose `applyTo` patterns match the file you
are editing. Where matching instructions conflict, prefer the rule specific to
that file over a general rule.

## Tooling

- Set up Python environments and run Python tools with `uv`, not `pip`. Where uv
  has no equivalent - `pip index versions`, `pip install --dry-run --report` -
  run pip through `uv run --no-project --with "pip>=22.2" pip ...` instead of
  installing it into the environment.
- `jq` and `git` are host requirements of the `Makefile` targets and the helpers
  in [`scripts/`](../../scripts/). A script that needs a host tool checks for it
  with `command -v` and names the tool to install when it is missing.
- A container image is the right tool when it carries setup worth pinning - an
  interpreter, a dependency set, a tool chain. It is the wrong tool when it only
  stands in for a tool the caller already needs on the host.
- Type checking runs through `scripts/mypy.bash` (`make -C clients/python mypy`),
  which uv resolves from `scripts/mypy/requirements.txt` on the interpreter that
  file pins. The `lint` workflow runs it, so it gates a pull request.

## Change discipline

- Keep changes focused on the requested behavior. Avoid unrelated refactors,
  formatting churn, or reordering.
- Change generated, vendored, or lock files only when the task requires it.
  Use the generation command documented in the file's header or in the owning
  client's `README.md`, never a manual edit.
- Do not add real secrets or credentials, including tokens and private keys,
  production endpoints, or environment-specific configuration to tracked files,
  fixtures, logs, or user-visible errors. Test fixtures may contain clearly
  synthetic credentials. Never copy credentials from real environments into
  tests.

## Tests and validation

- For behavior changes, add or update automated tests at the appropriate level.
  Use unit tests for pure logic, and end-to-end tests only for flows against a
  real deployment. Prefer unit tests to slow end-to-end tests.
- Prefer behavior-focused tests over tests coupled to private implementation.
  Avoid tautological assertions. Derive expected results from the required
  behavior or an independent reference, not by calling the implementation under
  test or copying its algorithm. Mock dependencies, not the behavior being
  tested. Checking only a mock's configured return value does not validate it.
- For a bug fix, add a regression test that fails before the fix and passes
  after it. If no such test is feasible, state the reason in the final chat
  response to the user under a heading named 'Validation'.
- Run the narrowest relevant validation available. Report which tests or checks
  you did not run and why.
- Run `pre-commit run --files <changed files>` and fix all findings. Never
  commit with `--no-verify`. If a pre-commit hook fails, fix the findings or
  explain them; do not bypass the hook.
- If a hook fails on pre-existing violations in a touched file, verify that your
  diff introduces zero new violations (compare `ruff check` output against
  `git show HEAD:<file> | ruff check --stdin-filename <file> -`) and fix every
  newly introduced violation before committing.

## Documentation

- Prefer clear code over comments that repeat it. Write comments in plain,
  specific language about intent, constraints, or non-obvious behavior. Omit
  boilerplate, decorative headings, and step-by-step narration.
- Unslop every comment you add or touch before committing, per
  [`unslop`](../skills/unslop/SKILL.md): facts only, no evaluative adjectives,
  no narration, and no fact repeated between a header and an inline comment.
- Update docs when a change affects public APIs, configuration, developer
  workflows, or user-visible behavior. The published site is built from
  [`docs/`](../../docs/) by `make docs`.
- Keep docs concise. Link to existing explanations rather than copying them.
  Retain brief local context where needed to understand or use the code.

## Git workflow

- Commit locally and stop. Do not push, force-push, create pull requests, or
  resolve review threads unless explicitly asked.
- Address code-review comments in new commits prefixed with the reviewer's
  handle (e.g. `@<reviewer> review: fix ...`), never by amending the reviewed
  commit, so reviewers can see the incremental fix and identify responses to
  their reviews.
- Create pull requests as drafts unless explicitly told otherwise. If intent is
  unclear, ask.
- Pull requests are squash-merged, so the pull request title becomes the commit
  message. Use the gitmoji prefix the template lists.

## Pull request descriptions

- Follow the structure of [PULL_REQUEST_TEMPLATE.md](../PULL_REQUEST_TEMPLATE.md).
- Always unslop before posting, whoever drafted the text. Run it through
  [`unslop`](../skills/unslop/SKILL.md) so the description carries only what
  changed and why.
- Open with the template's `## Goal` section: one sentence on why the PR exists.
- Keep them compact: state the final solution, the facts, and the measurements.
  No trial or process narrative, no step-by-step history of how the branch
  evolved.
- `## What do these changes do?`: state the change in behavior, not the diff.
  The review already shows the files, so name one only when that file is itself
  the subject (a generated client, the openapi specification, a lockfile, a
  config a reviewer must open); name a workflow by its display name, never its
  file name. Say nothing about code the PR does not touch. At most two sentences
  per bullet.
- Work that is not what the `## Goal` sentence is about goes under a
  `### Bonus` sub-title of `## What do these changes do?`, not mixed into the
  main bullets. Better still, put it in its own PR.
- Background a reviewer needs but did not ask for goes under a `### Context`
  sub-title: two sentences, facts or measurements only.
- `## How to test`: commands and snippets a reviewer runs, or `n/a`. What you
  ran while developing does not belong here, and nowhere else either.
- Work to do after merge goes under a `### Follow-up` sub-title, not in
  `## How to test`.
- Do not report tooling that runs by default. Pre-commit, linting, and the test
  suite passing is expected. Report only what a reviewer cannot infer:
  measurements, and what was deliberately left untested.
- Keep each bullet point to at most two sentences.
- State each fact once. A mechanism explained in one bullet must not come back
  in the next.
- Use the platform's own words: checks pass or fail, reviewers are requested. No
  `green`/`red`, no `paging the owners`, no metaphors (`once CI has spoken`):
  literal wording only.
- When the PR was AI generated, tick the box in `## AI assistance` and fill the
  `Assisted-by:` line.
- Fill every template section. When one does not apply, write `n/a`.
- Unslop means cutting filler openers and closers (`This PR aims to ...`,
  `Feel free to ask ...`), evaluative adjectives (`robust`, `seamless`,
  `comprehensive`), extra headings or summaries that duplicate the template
  sections — except `### Bonus`, `### Context`, and `### Follow-up` — and prose
  that restates the diff.
- Keep the caveats. Do not dress a known limitation in optimistic prose, and do
  not claim more than the measurements support.
- Performance PRs: include before/after measurements (e.g. CI step durations,
  baseline mean vs. new value). If the measurement is not available yet, leave an
  explicit placeholder and fill it in once CI completes.

## Ordering

- Insert new entries into hand-maintained unordered lists in alphabetical
  position. Do not reorder existing entries. Preserve order that affects
  behavior, such as precedence, dependencies, registration, or initialization.
- Use the configured formatter, linter, or generator to sort entries when it
  provides that function.
