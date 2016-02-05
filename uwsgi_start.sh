#!/usr/bin/env bash

# get script location

pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

cd ${SCRIPTPATH}

# Create/update virtualenv when starting the server
./make_venv.sh

# Launch uwsgi
uwsgi --module mass_server_flask \
    --callable app \
    --master \
    --http-socket localhost:8000 \
    --stats localhost:1717 \
    --home venv_mass \
    --vacuum \
    --workers 5 \
    --harakiri 20 \
    --max-requests 5000 \
    --enable-threads \
    --post-buffering 4096 \
    --pidfile=uwsgi.pid \
    --daemonize=uwsgi.log
