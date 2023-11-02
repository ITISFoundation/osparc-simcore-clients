#!/bin/bash

# Validate that a string is a valid semantic version
# This uses the regex pattern here: https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes


version=$1
validated_version=$(echo "${version}" | grep -E "^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$")
if [ -z "${validated_version}" ]; then
    echo "Received invalid semantic version: ${version}"
    exit 1
fi
echo -n "${validated_version}"
