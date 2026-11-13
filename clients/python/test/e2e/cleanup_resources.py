"""Deletes what a run left on the deployment named by the environment.

Run it after the suite, from a step that also runs when the tests fail. Tests delete their own
jobs and files, and so does the notebook test once its notebook finishes; this covers a run that
got killed before those teardowns ran, which is why it lives outside the pytest process.

What to delete comes from the log the run wrote as it created each resource, at the path in
OSPARC_E2E_RESOURCE_LOG. Deleting exactly what this run created cannot touch what a concurrent
run is waiting on. --all-jobs deletes every job of this user instead, for a leak with no log; it
covers jobs only, so a file with no log stays behind.

OSPARC_API_HOST, OSPARC_API_KEY and OSPARC_API_SECRET select the deployment, the same variables
the tests read. One deployment per invocation.
"""

import argparse
import logging
import os
from datetime import timedelta
from pathlib import Path

import osparc
import tenacity
from _utils import (
    RESOURCE_LOG_ENV_VAR,
    delete_recorded_resources,
    read_recorded_resources,
    sweep_all_jobs,
)
from urllib3.exceptions import HTTPError as Urllib3HttpError

_logger = logging.getLogger(__name__)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Delete what a run left behind on one deployment.",
        epilog=f"{RESOURCE_LOG_ENV_VAR} names the log to read when --resource-log is absent.",
    )
    parser.add_argument(
        "--resource-log",
        type=Path,
        default=None,
        help="the file the run recorded what it created in",
    )
    parser.add_argument(
        "--all-jobs",
        action="store_true",
        help="delete every job of this user rather than only the recorded resources",
    )
    parser.add_argument(
        "--retry-minutes",
        type=int,
        default=None,
        help="retry for this many minutes when the server answers with an API error. "
        "Without it, a single attempt is made.",
    )
    return parser.parse_args()


def _delete(args: argparse.Namespace, api_client: osparc.ApiClient) -> int:
    if args.all_jobs:
        return sweep_all_jobs(api_client)

    resource_log = args.resource_log or (
        Path(logged) if (logged := os.environ.get(RESOURCE_LOG_ENV_VAR)) else None
    )
    if resource_log is None:
        _logger.warning(
            "nothing to delete: no resource log, since %s is unset. Pass --resource-log, set "
            "the variable, or use --all-jobs",
            RESOURCE_LOG_ENV_VAR,
        )
        return 0

    recorded = read_recorded_resources(resource_log)
    _logger.info("Deleting %d resources recorded in %s", len(recorded), resource_log)
    return delete_recorded_resources(api_client, recorded)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = _parse_args()

    host = os.environ.get("OSPARC_API_HOST")
    username = os.environ.get("OSPARC_API_KEY")
    password = os.environ.get("OSPARC_API_SECRET")
    if not (host and username and password):
        _logger.error(
            "OSPARC_API_HOST, OSPARC_API_KEY and OSPARC_API_SECRET must be set"
        )
        return 1

    stop = (
        tenacity.stop_after_delay(timedelta(minutes=args.retry_minutes))
        if args.retry_minutes
        else tenacity.stop_after_attempt(1)
    )
    configuration = osparc.Configuration(
        host=host, username=username, password=password
    )
    try:
        with osparc.ApiClient(configuration=configuration) as api_client:
            for attempt in tenacity.Retrying(
                retry=tenacity.retry_if_exception_type(
                    (osparc.ApiException, Urllib3HttpError)
                ),
                stop=stop,
                wait=tenacity.wait_fixed(10),
                reraise=True,
            ):
                with attempt:
                    deleted = _delete(args, api_client)
    except Exception as exc:
        _logger.error("Failed to clean up %s: %s", host, exc)
        return 1

    _logger.info("Deleted %d resources on %s", deleted, host)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
