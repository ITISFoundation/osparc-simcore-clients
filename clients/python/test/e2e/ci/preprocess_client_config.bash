#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

doc="Setup client configuration for e2e testing of the osparc python client\n"
doc+="Input:\n"
doc+="------\n"
doc+="\tA single json string containing either the field osparc_client_version or the two fields osparc_client_repo and osparc_client_branch.\n"
doc+="\tosparc_client_version can either be the version of a client (e.g. \"0.5.0\") or \"latest\"\n"
doc+="\tExample 1: bash setup_client_config.bash '{\"osparc_client_repo\": \"ITISFoundation/osparc-simcore-clients\", \"osparc_client_branch\": \"master\"}'\n"
doc+="\tExample 2: bash setup_client_config.bash '{\"osparc_client_version\": \"0.5.0\"}'\n"
doc+="Output:\n"
doc+="-------\n"
doc+="\tA json string which, when passed to install_osparc_python_client.bash installs the wanted python client"

print_doc() { echo -e "$doc"; }
[ $# -eq 0 ] && print_doc && exit 0

osparc_client_workflow=publish-and-test-python-client
osparc_client_config=$1

# extract keys from input json
if [[ $(echo "$osparc_client_config" | jq 'has("osparc_client_version")') == "true" ]]; then
  if [[ $(echo "$osparc_client_config" | jq 'length') != 1 ]]; then
    echo "${osparc_client_config} was invalid"
    exit 1
  fi
else
  if [[ $(echo "$osparc_client_config" | jq 'length') != 2 ]]; then
    echo "${osparc_client_config} was invalid"
    exit 1
  fi
  if [[ $(echo "$osparc_client_config" | jq 'has("osparc_client_branch")') != "true" || $(echo "$osparc_client_config" | jq 'has("osparc_client_repo")') != "true" ]]; then
    echo "${osparc_client_config} was invalid"
    exit 1
  fi
  osparc_client_repo=$(echo "$osparc_client_config" | jq -r '.osparc_client_repo')
  osparc_client_branch=$(echo "$osparc_client_config" | jq -r '.osparc_client_branch')
  osparc_client_runid=$(gh run list --repo="${osparc_client_repo}" --branch="${osparc_client_branch}" --workflow="${osparc_client_workflow}" --limit=100 --json=databaseId,status --jq='map(select(.status=="completed")) | .[0].databaseId')
  osparc_client_config=$(echo "${osparc_client_config}" | jq --arg cwfw "${osparc_client_workflow}" '. += {"osparc_client_workflow": $cwfw}')
  osparc_client_config=$(echo "${osparc_client_config}" | jq --arg crid "${osparc_client_runid}" '. += {"osparc_client_runid": $crid}')
fi

echo "${osparc_client_config}"
