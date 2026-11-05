---
name: unslop
description: >-
  Rewrites AI-flavoured prose in this repository — pull request descriptions,
  commit messages, documentation, comments — into plain factual text a reviewer
  can act on. Use when: unslop, de-slop, clean up or rewrite this PR
  description, tighten a commit message, remove filler or marketing tone from
  docs or comments.
---

# Unslop

Rewrite drafted text so one read answers: what changed, why, and what was
measured. Facts in, adjectives out.

## When to use

- A pull request description was drafted by an agent, or grew while the branch
  was built and now narrates that history.
- A commit message needs tightening before it is pushed.
- Documentation, docstrings or code comments read like product copy.

## What counts as slop

- **Filler openers and closers** — `This PR aims to provide ...`,
  `Feel free to ask ...`. Delete; start with the change itself.
- **Process narration** — `first I tried X, then moved to Y`. Drop the trail.
  Keep the final design and the reason it won.
- **Evaluative adjectives** — robust, seamless, comprehensive, elegant,
  best-practice. Delete them, or replace the claim with the measurement.
- **Restating the diff** — `Added foo() in bar.py`. The diff already says it;
  say what it is good for instead.
- **Duplicated structure** — a `## Summary` inside a body that follows the
  template. Use the template sections and nothing else.
- **Hedging next to a claim** — `should mostly improve build times`. Either give
  the number or write `not measured yet`.
- **Fake completeness** — `completely solves the issue`. State what it fixes and
  what it leaves open.
- **Formatting theatre** — check-mark and rocket bullets, bullet towers, bolded
  sentences. Plain sentences and one-level lists.
- **Leftover boilerplate** — an empty `## How to test` or `N/A`. Fill it or
  delete the section.

## Workflow

1. Read the text as its reviewer: what decision or check does it need from me?
2. Rewrite in place, keeping the structure that audience expects — for pull
   requests that is
   [PULL_REQUEST_TEMPLATE.md](../../PULL_REQUEST_TEMPLATE.md).
3. Preserve every fact, number, link, GitHub reference (`#1234`), file path and
   command exactly. Never invent a measurement to replace a vague claim; verify
   it or write `not measured yet`.
4. Keep the conventions the repository depends on: the gitmoji title prefix, the
   `Co-authored-by:` trailer, and fenced code blocks.
5. Cut until every sentence either changes what a reader does or tells them a
   fact they could not get from the diff.
6. Show the rewritten text, not a description of it, and only then post or push.

## Do not

- Do not touch code, tests or configuration. Text only.
- Do not soften a limitation, a failing check, or a known follow-up.
- Do not raise the register: `utilize`, `leverage`, `delve` are not fixes.
- Do not add emoji, badges or sections the template does not have.

## Before and after

Before:

```text
🚀 This PR aims to provide a robust and seamless upload experience! We first
tried keeping the client-side checksum dedup, then moved to relying on the
server, which comprehensively removes a whole class of duplicate-upload bugs.

## Summary
- ✨ Streamlined uploads
- ✅ Improved reliability
```

After:

```text
The client-side checksum dedup dropped a file whose checksum the server did not
know yet, so uploads of identical files raced and one of them was lost
(reported on the staging deployment, reproduced by `test_files_api.py`). The
dedup map is removed and the server's response is now the source of truth.

`upload_file_from_path` still returns `None` on a 404, which is unchanged.
```
