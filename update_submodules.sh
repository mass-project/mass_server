#!/usr/bin/env bash
set -e

# get script location

pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

cd ${SCRIPTPATH}

git submodule init
git submodule update
