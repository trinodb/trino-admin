#!/usr/bin/env bash

set -xeuo pipefail

function usage() {
  cat << EOF
build-artifacts-in-docker.sh [--root_dir <dir>] [--base_image_name <name>] [--base_image_tag <tag>] [--online-dist] [--offline-dist]

This script is used to build the offline and/or online distributions of presto-admin in the specified Docker image name.
  --root_dir <dir>:         Directory on local filesystem where the presto-admin tree is located. Defaults to this
                            script's current directory.
  --base_image_name <name>: Name of Docker image to use during the build. Defaults to prestodev/centos6-presto-admin-tests.
  --base_image_tag <tag>:   Tag of the Docker image to use during the build. Defaults to the tag stored in the base_images_tag.json file.
  --online-dist:            Boolean argument indicating whether the online distribution should be build. If neither the
                            --online-dist nor the --offline-dist flags are specified then both distributions are built.
  --offline-dist:           Boolean argument indicating whether the offline distribution should be build. If neither the
                            --online-dist nor the --offline-dist flags are specified then both distributions are built.
EOF
}

DIST_TARGETS=""

while [[ $# -gt 0 ]]
do
  key="$1"

  case $key in
      --root_dir)
      ROOT_DIR="$2"
      shift
      shift
      ;;
      --base_image_name)
      BASE_IMAGE_NAME="$2"
      shift
      shift
      ;;
      --base_image_tag)
      BASE_IMAGE_TAG="$2"
      shift
      shift
      ;;
      --online-dist)
      DIST_TARGETS="$DIST_TARGETS dist-online "
      shift
      ;;
      --offline-dist)
      DIST_TARGETS="$DIST_TARGETS dist-offline "
      shift
      ;;
      *)    # unknown; show usage and error out
      echo "Unknown option $key"
      usage
      exit 1
      ;;
  esac
done

ROOT_DIR=${ROOT_DIR:-"$(readlink -f $(dirname $0)/..)"}
BASE_IMAGE_NAME=${BASE_IMAGE_NAME:-"prestodev/centos6-presto-admin-tests"}
BASE_IMAGE_TAG=${BASE_IMAGE_TAG:-"$(cat ${ROOT_DIR}/base-images-tag.json | python -c 'import sys, json; print json.load(sys.stdin)["base_images_tag"]')"}
DIST_TARGETS=${DIST_TARGETS:-"dist-online dist-offline"}

BASE_IMAGE_NAME=${BASE_IMAGE_NAME}-build

echo Building presto-admin-artifacts in container ${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG}

CONTAINER_NAME="presto-admin-build-$(date '+%s')"
CONTAINER_DIR="/mnt/presto-admin"

docker run --name ${CONTAINER_NAME} -v ${ROOT_DIR}:${CONTAINER_DIR} --rm -i ${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG} \
  env CONTAINER_DIR="${CONTAINER_DIR}" env DIST_TARGETS="${DIST_TARGETS}" bash <<"EOF"
    set -x
    cd ${CONTAINER_DIR}
    pip install --upgrade pycparser==2.18
    pip install --upgrade cffi==1.11.5
    pip install --upgrade PyNaCl==1.2.1
    pip install --upgrade idna==2.1 cryptography==2.1.1
    pip install --upgrade pip==9.0.2
    pip install --upgrade wheel==0.23.0
    pip install --upgrade setuptools==20.1.1
    export PYTHONPATH=${PYTHONPATH}:$(pwd)
    make ${DIST_TARGETS}
EOF
