#!/bin/bash
# http://redsymbol.net/articles/unofficial-bash-strict-mode/

set -o errexit
set -o nounset
set -o pipefail
IFS=$'\n\t'

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
IMAGE_NAME="local/scripts-$(basename "$0"):latest"
WORKDIR="$(pwd)"

# mypy only reads `[tool.mypy]` from a file named `pyproject.toml` (it picks the
# parser from the file name), so the config has to keep its name when it is
# mounted into the container.
DEFAULT_MYPY_CONFIG="$(git rev-parse --show-toplevel)/clients/python/pyproject.toml"
MYPY_CONFIG=$(realpath "${MYPY_CONFIG:-${DEFAULT_MYPY_CONFIG}}")
MYPY_CONFIG_BASENAME="$(basename "${MYPY_CONFIG}")"

build() {
  echo Building image "$IMAGE_NAME"
  #
  docker buildx build \
    --load \
    --quiet \
    --tag "$IMAGE_NAME" \
    "$SCRIPT_DIR/mypy"
}

echo_requirements() {
  echo "Installed :"
  docker run \
    --interactive \
    --rm \
    --user="$(id --user "$USER")":"$(id --group "$USER")" \
    --entrypoint="uv" \
    "$IMAGE_NAME" \
    --no-cache-dir pip freeze
}

run() {
  echo Using "$(docker run --rm "$IMAGE_NAME" --version)"
  echo "Mypy config ${MYPY_CONFIG} mounted as /config/${MYPY_CONFIG_BASENAME}"
  echo Mypying "$(realpath "$@")":
  #
  docker run \
    --rm \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --user="$(id --user "$USER")":"$(id --group "$USER")" \
    --volume "$MYPY_CONFIG":"/config/${MYPY_CONFIG_BASENAME}" \
    --volume "$WORKDIR":/src \
    --workdir=/src \
    "$IMAGE_NAME" \
    --config-file "/config/${MYPY_CONFIG_BASENAME}" \
    "$@"
}

# ----------------------------------------------------------------------
# MAIN
#
# USAGE
#    ./scripts/mypy.bash <path>...                    # uses clients/python/pyproject.toml
#    MYPY_CONFIG=<file> ./scripts/mypy.bash <path>... # any `mypy.ini` or `pyproject.toml`
build
echo_requirements
run "$@"
echo "DONE"
# ----------------------------------------------------------------------
