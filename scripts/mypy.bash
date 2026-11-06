#!/bin/bash
# http://redsymbol.net/articles/unofficial-bash-strict-mode/

set -o errexit
set -o nounset
set -o pipefail
IFS=$'\n\t'

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

# mypy picks the parser from the file name, so `[tool.mypy]` has to stay in a pyproject.toml.
DEFAULT_MYPY_CONFIG="$(git rev-parse --show-toplevel)/clients/python/pyproject.toml"
MYPY_CONFIG=$(realpath "${MYPY_CONFIG:-${DEFAULT_MYPY_CONFIG}}")

# Pinned here rather than taken from the environment. Why the interpreter is 3.10 and not
# the 3.9 floor is recorded in clients/python/pyproject.toml; the package versions are in
# scripts/mypy/requirements.txt.
MYPY_PYTHON_VERSION="3.10"
MYPY_REQUIREMENTS="${SCRIPT_DIR}/mypy/requirements.txt"

uv_mypy() {
  uv run \
    --no-project \
    --python "${MYPY_PYTHON_VERSION}" \
    --with-requirements "${MYPY_REQUIREMENTS}" \
    mypy \
    --warn-unused-configs \
    --config-file "${MYPY_CONFIG}" \
    "$@"
}

echo_requirements() {
  echo "Installed :"
  # Resolved versions of what scripts/mypy/requirements.txt asks for, read inside the
  # environment mypy runs in.
  uv run \
    --no-project \
    --python "${MYPY_PYTHON_VERSION}" \
    --with-requirements "${MYPY_REQUIREMENTS}" \
    python -c '
import re
import sys
from importlib import metadata

print(sys.version)
for line in open(sys.argv[1]):
    name = re.split(r"[<>=!~;\[ ]", line.strip(), maxsplit=1)[0].strip()
    if not name or name.startswith("#"):
        continue
    try:
        print(f"{name}=={metadata.version(name)}")
    except metadata.PackageNotFoundError:
        print(f"{name}: not found")
' "${MYPY_REQUIREMENTS}"
}

run() {
  echo Using "$(uv_mypy --version)"
  echo "Mypy config ${MYPY_CONFIG}"
  echo Mypying "$(realpath "$@")":
  uv_mypy "$@"
}

# ----------------------------------------------------------------------
# MAIN
#
# USAGE
#    ./scripts/mypy.bash <path>...                    # uses clients/python/pyproject.toml
#    MYPY_CONFIG=<file> ./scripts/mypy.bash <path>... # any `mypy.ini` or `pyproject.toml`
echo_requirements
run "$@"
echo "DONE"
# ----------------------------------------------------------------------
