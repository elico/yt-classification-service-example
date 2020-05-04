#!/usr/bin/env bash 

set -xe

DEBUG_MODE="1"
RELEASE_NUMBER="1"
VERSION_NUMBER="1.1.41"

BUILD_ARRAY=`ls -d redwood-*/`

NOCACHE=$(cat no-cache)

if [[ ! -z "${BUILD_ONLY}" ]];then
	BUILD_ARRAY=`ls -d */|egrep "${BUILD_ONLY}"`
fi

#for Build in `find ./ -type d -maxdepth 1`
for Build in ${BUILD_ARRAY}
do
	echo $Build
	cd "$Build"
	DOCKER_IMAGE=`cat dockerimage`
	echo "${DOCKER_IMAGE}"
	stat build && stat dockerimage && \
		 docker build  . -t "${DOCKER_IMAGE}" ${NOCACHE} && \
	stat build && docker run -it \
	        -e COMPRESSION="${COMPRESSION}" \
	        -e DEBUG_MODE="${DEBUG_MODE}" \
	        -e RELEASE_NUMBER="${RELEASE_NUMBER}" \
	        -e VERSION_NUMBER="${VERSION_NUMBER}" \
	        -v `pwd`/srv:/srv \
	                "${DOCKER_IMAGE}"
	cd -
done

set +xe
