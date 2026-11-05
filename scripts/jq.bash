#!/bin/bash


if command -v jq &> /dev/null; then
    jq "$@"
else
    source $(dirname "$0")/jq/config.bash

    inputs=()

    mount_str=""
    for var in "$@"
    do
        if [ -f "${var}" ]; then
            host_dir="$(dirname "$(realpath "${var}")")"
            container_dir="/local/$(basename "${host_dir}")"
            mount_str="--volume=${host_dir}:${container_dir}"
            file="${container_dir}/$(basename "${var}")"
            inputs+=("${file}")
        else
            inputs+=("${var}")
        fi
    done

    docker run --rm -t "${mount_str}" "${IMAGE_NAME}":"${IMAGE_VERSION}" "${inputs[@]}"
fi
