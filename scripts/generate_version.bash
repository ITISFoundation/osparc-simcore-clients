#!/bin/bash

# Generate semantic version which is one patch greater than the latest released version
# This is done by inspecting the tags on the git repo https://github.com/ITISFoundation/osparc-simcore-clients

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

latest=$(git ls-remote --tags --refs --sort=version:refname https://github.com/ITISFoundation/osparc-simcore-clients \
  | tail -1 \
  | grep -oP '(?<=refs/tags/v)\d+\.\d+\.\d+')
new_version=$(echo "${latest}" | sed -E 's/([0-9]+\.[0-9]+\.)([0-9]+)/echo "\1$((\2+1))"/e')
echo -n "${new_version}"
