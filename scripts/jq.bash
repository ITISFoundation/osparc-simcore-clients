#!/bin/bash
# A host check, not a substitute for installing jq: `make info-tools` reads
# `jq --version` and osparc_version.bash calls jq directly.

set -o errexit
set -o nounset
set -o pipefail

if ! command -v jq >/dev/null 2>&1; then
    echo "jq is required but not installed. Install it (e.g. 'apt-get install jq' or 'brew install jq')." >&2
    exit 1
fi

exec jq "$@"
