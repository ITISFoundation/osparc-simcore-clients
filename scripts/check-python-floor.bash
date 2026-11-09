#!/usr/bin/env bash
# Fails when the Python floor this repo declares stops agreeing with itself.
#
# None of these tools can read a shared declaration: ruff wants `target-version`, vermin
# wants `--target`, setuptools wants `python_requires`, mypy wants `python_version`, and CI
# lists what it actually tests. The floor therefore lives in several places, and this checks
# they still say the same thing.
# The lowest `Programming Language :: Python :: 3.X` classifier is included because it is
# what the package advertises to pip and PyPI.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

failures=0
seen=()

declare_value() { # <where the value comes from> <minor version>
    seen+=("$2 $1")
    if [ -z "$2" ]; then
        echo "check-python-floor: cannot read $1" >&2
        failures=1
    fi
}

declare_value "python_requires in clients/python/setup.py" \
    "$(sed -nE 's/.*"python_requires": ">=3\.([0-9]+)".*/\1/p' clients/python/setup.py | head -1)"
declare_value "lowest classifier in clients/python/setup.py" \
    "$(sed -nE 's/.*Programming Language :: Python :: 3\.([0-9]+).*/\1/p' clients/python/setup.py | sort -n | head -1)"
declare_value "target-version in ruff.toml" \
    "$(sed -nE 's/target-version = "py3([0-9]+)".*/\1/p' ruff.toml)"
declare_value "--target of the vermin hook in .pre-commit-config.yaml" \
    "$(sed -nE 's/.*--target=3\.([0-9]+)-.*/\1/p' .pre-commit-config.yaml | head -1)"
declare_value "python_version in clients/python/pyproject.toml" \
    "$(sed -nE 's/^python_version = "3\.([0-9]+)".*/\1/p' clients/python/pyproject.toml)"
declare_value "lowest entry of the test matrix in .github/workflows/build-python-client.yml" \
    "$(sed -nE 's/.*python-version: \[(.*)\].*/\1/p' .github/workflows/build-python-client.yml |
        tr -d '"' | tr ',' '\n' | grep -oE '3\.[0-9]+' | cut -d. -f2 | sort -n | head -1)"

# python_requires sets the floor, everything else has to match it
floor="${seen[0]%% *}"
if [ -z "$floor" ]; then
    exit "$failures"
fi
for entry in "${seen[@]:1}"; do
    if [ "${entry%% *}" != "$floor" ]; then
        echo "check-python-floor: ${entry#* } says 3.${entry%% *}, python_requires says 3.$floor" >&2
        failures=1
    fi
done

exit "$failures"
