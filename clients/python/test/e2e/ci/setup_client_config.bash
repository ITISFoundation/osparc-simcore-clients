#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

doc="Setup client configuration for e2e testing of the osparc python client\n"
doc+="Input:\n"
doc+="------\n"
doc+="\tA single json string containing the three fields OSPARC_CLIENT_VERSION, OSPARC_CLIENT_REPO and OSPARC_CLIENT_BRANCH and meeting exactly one of the following two conditions:\n"
doc+="\t\t- the field OSPARC_CLIENT_VERSION is empty\n"
doc+="\t\t- the two fields OSPARC_CLIENT_REPO and OSPARC_CLIENT_BRANCH are empty\n"
doc+="\tOSPARC_CLIENT_VERSION can either be the version of a client (e.g. \"0.5.0\") or \"latest\"\n"
doc+="\tExample 1: bash setup_client_config.bash '{\"OSPARC_CLIENT_REPO\": \"ITISFoundation/osparc-simcore-clients\", \"OSPARC_CLIENT_BRANCH\": \"master\", \"OSPARC_CLIENT_VERSION\": \"\"}'\n"
doc+="\tExample 2: bash setup_client_config.bash '{\"OSPARC_CLIENT_REPO\": \"\", \"OSPARC_CLIENT_BRANCH\": \"\", \"OSPARC_CLIENT_VERSION\": \"0.5.0\"}'\n"
doc+="Output:\n"
doc+="-------\n"
doc+="\tA json string which, when passed to install_osparc_python_client.bash installs the wanted python client"

print_doc() { echo -e "$doc"; }
[ $# -eq 0 ] && print_doc && exit 0

OSPARC_CLIENT_WORKFLOW=publish-and-test-python-client
OSPARC_CLIENT_CONFIG=$1

# extract keys from input json
OSPARC_CLIENT_REPO=$(echo "${OSPARC_CLIENT_CONFIG}" | jq -r .OSPARC_CLIENT_REPO)
OSPARC_CLIENT_BRANCH=$(echo "${OSPARC_CLIENT_CONFIG}" | jq -r .OSPARC_CLIENT_BRANCH)
OSPARC_CLIENT_VERSION=$(echo "${OSPARC_CLIENT_CONFIG}" | jq -r .OSPARC_CLIENT_VERSION)
NKEYS=$(echo "${OSPARC_CLIENT_CONFIG}" | jq 'keys | length ')
if [[ "${NKEYS}" != 3 ]]; then
  print_doc
  exit 1
fi

# sanity check inputs: either CLIENT_VERSION must be passed, xor CLIENT_REPO, CLIENT_BRANCH
if [[ -z ${OSPARC_CLIENT_VERSION} ]] && [[ -z ${OSPARC_CLIENT_REPO} && -z ${OSPARC_CLIENT_BRANCH} ]]; then
  print_doc
  exit 1
fi
if [[ -n ${OSPARC_CLIENT_VERSION} ]] && [[ -n ${OSPARC_CLIENT_REPO} || -n ${OSPARC_CLIENT_BRANCH} ]]; then
  print_doc
  exit 1
fi


# add entries to CLIENT_CONFIG to fix installation
if [[ -n ${OSPARC_CLIENT_REPO} ||  -n ${OSPARC_CLIENT_BRANCH} ]]; then
  if [[ -z ${OSPARC_CLIENT_REPO} || -z ${OSPARC_CLIENT_BRANCH} ]]; then
    print_doc
    exit 1
  fi
  OSPARC_CLIENT_RUNID=$(gh run list --repo="${OSPARC_CLIENT_REPO}" --branch="${OSPARC_CLIENT_BRANCH}" --workflow="${OSPARC_CLIENT_WORKFLOW}" --limit=100 --json=databaseId,status --jq='map(select(.status=="completed")) | .[0].databaseId')
  OSPARC_CLIENT_CONFIG=$(echo "${OSPARC_CLIENT_CONFIG}" | jq --arg cwfw "${OSPARC_CLIENT_WORKFLOW}" '. += {"OSPARC_CLIENT_WORKFLOW": $cwfw}')
  OSPARC_CLIENT_CONFIG=$(echo "${OSPARC_CLIENT_CONFIG}" | jq --arg crid "${OSPARC_CLIENT_RUNID}" '. += {"OSPARC_CLIENT_RUNID": $crid}')
fi

echo "${OSPARC_CLIENT_CONFIG}"
