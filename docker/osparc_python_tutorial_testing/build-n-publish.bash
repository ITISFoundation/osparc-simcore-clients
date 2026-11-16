#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

# the image is built from this directory, whatever the caller's working directory is
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

command -v docker >/dev/null || { echo "Install docker first" >&2; exit 1; }
docker buildx version >/dev/null 2>&1 || { echo "Install docker buildx first" >&2; exit 1; }

IMAGE_NAME="itisfoundation/osparc_python_tutorial_testing"
# Publish a new tag, never republish one in place: the e2e-portal GitLab CI pins an exact tag
# (`PYTHON_CLIENT_E2E_IMAGE` in its `.gitlab-ci.yml`), so the order is bump here, publish,
# then bump the pin there. Published tags:
#   v1 py3.9 without uv, v2 py3.9 + uv, v3 py3.11 on bookworm, v4 py3.11 on Debian trixie,
#   v5 same content plus OCI provenance labels and a multi-arch amd64 + arm64 manifest.
IMAGE_VERSION="v5"

# Multi-arch: the bases (python:3.11-slim-trixie, uv) ship manifests for both architectures
# and no layer here is arch-specific, so one buildx run publishes a manifest list. A plain
# `docker build` publishes only the build host's architecture.
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --build-arg "BUILD_GIT_REVISION=$(git rev-parse --short HEAD)" \
    --build-arg "BUILD_VERSION=${IMAGE_VERSION}" \
    --build-arg "BUILD_CREATED=$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    --tag "${IMAGE_NAME}:${IMAGE_VERSION}" \
    --push \
    .
