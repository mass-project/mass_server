#!/usr/bin/env bash
set -e

# get script location

pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

cd ${SCRIPTPATH}

# set python version
PYTHON_BIN=$(which python3)

# set venv name
VENV=venv_mass

# delete previous virtual environment if existing
rm -rf ${VENV}

# create new virtual environment
virtualenv --python ${PYTHON_BIN} --no-site-packages ${VENV}

# activate virtual environment
source ${VENV}/bin/activate

# install required packages
pip install -r requirements.txt
