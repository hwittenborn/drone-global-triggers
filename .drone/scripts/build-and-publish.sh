#!/usr/bin/env bash
set -ex

# Login.
echo "${proget_api_key}" | docker login -u api \
                                        --password-stdin \
                                        "${proget_server}"

# Build.
docker build --pull \
             --no-cache \
             --tag "${proget_server}/docker/hwittenborn/drone-global-triggers" \
             ./

# Publish.
docker push "${proget_server}/docker/hwittenborn/drone-global-triggers"
