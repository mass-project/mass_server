#!/usr/bin/env bash
set -e

# get script location

pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

cd ${SCRIPTPATH}

# Create/update virtualenv when starting the server
./make_venv.sh

source venv_mass/bin/activate

export CONFIG_PATH=mass_flask_config.config_testing.TestingConfig

nosetests \
    --verbosity 2 \
    --with-coverage \
    --cover-package=mass_flask_api \
    --cover-package=mass_flask_core \
    --cover-package=mass_flask_config \
    --cover-inclusive \
    --cover-erase \
    --cover-branches \
    --cover-xml \
    --with-xunit \
    --exclude-dir=./venv_mass/
