#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

version=$1
report=$(mktemp)
trap 'rm -rf "${report}"' EXIT

# pip, run through uv: `uv pip install` has no `--report`, and the JSON installation
# report is what this script reads the resolved version from. The floor matters
# because uv reuses the interpreter's own pip when that already satisfies it, and
# `install --dry-run --report` exists only from pip 22.2 on.
PIP_RUN=(uv run --no-project --quiet --with "pip>=22.2" pip)

if [ "${version}" == "latest_release" ]; then
    "${PIP_RUN[@]}" install osparc --force-reinstall --dry-run --quiet --report "${report}"
elif [ "${version}" == "latest_master" ]; then
    "${PIP_RUN[@]}" install osparc --pre --force-reinstall --dry-run --quiet --report "${report}"
else
    "${PIP_RUN[@]}" install "osparc==${version}" --force-reinstall --dry-run --quiet --report "${report}"
fi
jq -r '.install[] | select(.metadata.name == "osparc") | .metadata.version' "${report}"
