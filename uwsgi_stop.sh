#!/usr/bin/env bash

pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

cd ${SCRIPTPATH}

# Stop the server
uwsgi --stop uwsgi.pid
