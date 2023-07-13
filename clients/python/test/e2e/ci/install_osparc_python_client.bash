#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

doc="error"

print_doc() { echo -e "$doc"; }
[ $# -eq 0 ] && print_doc && exit 0

OSPARC_CLIENT_CONFIG=$1


OSPARC_CLIENT_VERSION=$(echo "${OSPARC_CLIENT_CONFIG}" | jq -r .OSPARC_CLIENT_VERSION)


if [[ -z ${OSPARC_CLIENT_VERSION} ]]; then
  OSPARC_CLIENT_REPO=$(echo "${OSPARC_CLIENT_CONFIG}" | jq -r .OSPARC_CLIENT_REPO)
  OSPARC_CLIENT_RUNID=$(echo "${OSPARC_CLIENT_CONFIG}" | jq -r .OSPARC_CLIENT_RUNID)
  TMPDIR=$(mktemp -d)
  pushd "${TMPDIR}"
  gh run download "${OSPARC_CLIENT_RUNID}" --repo="${OSPARC_CLIENT_REPO}"
  popd
  OSPARC_WHEEL=$(ls "${TMPDIR}"/osparc_python_wheels/osparc-*.whl)
  python -m pip install "${OSPARC_WHEEL}" --find-links="${TMPDIR}"/osparc_python_wheels --force-reinstall
  rm -rf "${TMPDIR}"
else
  V_STRING=""
  if [[ "${OSPARC_CLIENT_VERSION}" != "latest" ]]; then
    V_STRING="==${OSPARC_CLIENT_VERSION}"
  fi
  python -m pip install osparc"${V_STRING}" --force-reinstall
fi
