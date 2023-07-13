#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

usage() { echo "$0 options (e.g. '-r ITISFoundation/osparc-simcore -b master'):" && grep " .)\ #" "$0"; exit 0;}
[ $# -eq 0 ] && usage
CLIENT_WORKFLOW=publish-and-test-python-client
SCRIPTS_DIR=$(realpath "$(dirname "$0")")

unset CLIENT_REPO
unset CLIENT_BRANCH
unset CLIENT_VERSION

while getopts ":r:b:v" arg; do
  case $arg in
    r) # Define which repository to pick the client from
      ARG=${OPTARG:-}
      if [[ -n ${ARG} ]]; then
        CLIENT_REPO="${ARG}"
        echo "CLIENT_REPO=${CLIENT_REPO}"
      fi
      ;;
    b) # Define which branch to pick the client from
      ARG=${OPTARG:-}
      if [[ -n ${ARG} ]]; then
        CLIENT_BRANCH="${ARG}"
        echo "CLIENT_BRANCH=${CLIENT_BRANCH}"
      fi
      ;;
    v) # Define which version to install from PyPi. Use "-v latest" to install the latest version available on PyPi
      ARG=${OPTARG:-}
      if [[ -n ${ARG} ]]; then
        CLIENT_VERSION="${ARG}"
        echo "CLIENT_VERSION=${CLIENT_VERSION}"
      fi
      ;;
    *)
      echo "Recieved unknown flag"
      exit 1
      ;;
  esac
done

# sanity check inputs: either CLIENT_VERSION must be passed, xor CLIENT_REPO, CLIENT_BRANCH
ERR_MSG="Either a version (-v) must be passed as argument xor a pair repository and branch (-r and -v)"
if [[ ! -v CLIENT_VERSION ]] && [[ ! -v CLIENT_REPO || ! -v CLIENT_BRANCH ]]; then
  echo "${ERR_MSG}"
  exit 1
fi
if [[ -v CLIENT_VERSION ]] && [[ -v CLIENT_REPO ]] && [[ -v CLIENT_BRANCH ]]; then
  echo "${ERR_MSG}"
  exit 1
fi

if [[ -v CLIENT_REPO && -v CLIENT_BRANCH ]]; then
  tmp_dir=$(mktemp -d)
  echo "Using CLIENT_REPO=${CLIENT_REPO}, CLIENT_BRANCH=${CLIENT_BRANCH}, CLIENT_WORKFLOW=${CLIENT_WORKFLOW}"
  run_id=$(bash "${SCRIPTS_DIR}/gh.bash" run list --repo="${CLIENT_REPO}" --branch="${CLIENT_BRANCH}" --workflow=${CLIENT_WORKFLOW} --limit=25 --json=databaseId,status --jq='map(select(.status=="completed")) | .[0].databaseId')
  echo "Run id for latest completed '${CLIENT_WORKFLOW}' workflow on branch '${CLIENT_BRANCH}' in repo '${CLIENT_REPO}': ${run_id}"
  pushd "${tmp_dir}"
  bash "${SCRIPTS_DIR}"/gh.bash run download "${run_id}" --repo="${CLIENT_REPO}"
  popd
  osparc_wheel=$(ls "${tmp_dir}"/osparc_python_wheels/osparc-*.whl)
  python -m pip install "${osparc_wheel}" --find-links="${tmp_dir}"/osparc_python_wheels --force-reinstall
  rm -rf "${tmp_dir}"
elif [[ -v CLIENT_VERSION ]]; then
  echo "Using CLIENT_VERSION=${CLIENT_VERSION}"
  V_STRING=""
  if [[ "${CLIENT_VERSION}" != "latest" ]]; then
    V_STRING="==${CLIENT_VERSION}"
  fi
  python -m pip install osparc"${V_STRING}" --force-reinstall
fi
