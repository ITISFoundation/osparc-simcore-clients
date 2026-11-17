# ruff: noqa: B008  # typer reads its arguments from the argument defaults, so calling
# typer.Argument there is the documented shape of its API.
"""Gathers the e2e junit reports into one client-against-deployment table.

Every cell of the matrix, one client config against one deployment, runs as its own job because it
needs that deployment's credentials, and each writes its own junit report. This reads them back
together and prints one markdown table: rows are deployments, columns are client versions.

The two identities come from the junit properties the suite records in conftest.py
(record_run_in_junit). A report from a suite that predates those properties falls back to the path,
which says less but still separates the cells.

    python test/e2e/scripts/summarize_junit.py <dir-with-junit-xml>

Exits nonzero when a report carries a failure or an error, or when no report is found.
"""

import xml.etree.ElementTree as ElementTree
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import typer

_DEPLOYMENT_PROPERTY: Final[str] = "osparc_deployment"
_CLIENT_PROPERTY: Final[str] = "osparc_client_version"


@dataclass
class _Run:
    """One testsuite of one junit report."""

    deployment: str
    client: str
    passed: int
    failed: int
    errored: int
    skipped: int

    @property
    def unsuccessful(self) -> int:
        return self.failed + self.errored

    def __str__(self) -> str:
        counts = [f"{self.passed} passed"]
        if self.failed:
            counts.append(f"{self.failed} failed")
        if self.errored:
            counts.append(f"{self.errored} error")
        if self.skipped:
            counts.append(f"{self.skipped} skipped")
        return ", ".join(counts)


def _attribute(suite: ElementTree.Element, name: str) -> int:
    return int(suite.get(name, 0))


def _read_run(path: Path, suite: ElementTree.Element) -> _Run:
    properties = {
        element.get("name", ""): element.get("value", "")
        for element in suite.findall("properties/property")
    }
    tests = _attribute(suite, "tests")
    failed = _attribute(suite, "failures")
    errored = _attribute(suite, "errors")
    skipped = _attribute(suite, "skipped")
    return _Run(
        # Without the recorded properties the report says nothing about where it ran, so the
        # directory and file names are the only identity left.
        deployment=properties.get(_DEPLOYMENT_PROPERTY) or path.parent.name,
        client=properties.get(_CLIENT_PROPERTY) or path.name,
        passed=max(tests - failed - errored - skipped, 0),
        failed=failed,
        errored=errored,
        skipped=skipped,
    )


def read_runs(artifacts_dir: Path) -> list[_Run]:
    """Reads every junit report below artifacts_dir, one _Run per testsuite."""
    if not artifacts_dir.is_dir():
        raise typer.BadParameter(f"{artifacts_dir} is not a directory")

    runs: list[_Run] = []
    for path in sorted(artifacts_dir.rglob("*.xml")):
        root = ElementTree.parse(path).getroot()
        suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
        runs.extend(_read_run(path, suite) for suite in suites)
    return runs


def _merge(group: list[_Run]) -> str:
    """One cell for all reports of one deployment and client version."""
    if not group:
        return "n/a"
    return str(
        _Run(
            deployment="",
            client="",
            passed=sum(run.passed for run in group),
            failed=sum(run.failed for run in group),
            errored=sum(run.errored for run in group),
            skipped=sum(run.skipped for run in group),
        )
    )


def markdown_table(runs: list[_Run]) -> str:
    deployments = sorted({run.deployment for run in runs})
    clients = sorted({run.client for run in runs})
    lines = [
        "| deployment | " + " | ".join(clients) + " |",
        "| --- |" + " --- |" * len(clients),
    ]
    for deployment in deployments:
        cells = [
            _merge(
                [
                    run
                    for run in runs
                    if run.deployment == deployment and run.client == client
                ]
            )
            for client in clients
        ]
        lines.append(f"| {deployment} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main(artifacts_dir: Path = typer.Argument(...)) -> None:
    """Print the table and fail when a cell did not pass."""
    runs = read_runs(artifacts_dir)
    if not runs:
        typer.echo(f"no junit report found below {artifacts_dir}")
        raise typer.Exit(code=1)

    typer.echo(markdown_table(runs))
    if any(run.unsuccessful for run in runs):
        raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(main)
