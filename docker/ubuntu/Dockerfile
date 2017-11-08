FROM ubuntu:latest

ARG BRANCH=master
ENV BRANCH ${BRANCH}

# Install dependencies
RUN apt-get update && apt-get -y install libffi-dev automake autoconf libtool python3 python3-dev python3-pip git tzdata

# Install MASS server
RUN BUILD_LIB=1 pip3 install git+https://github.com/mass-project/mass_server.git@$BRANCH

# Create MASS user
RUN useradd -m mass
USER mass
WORKDIR /home/mass

# Run uwsgi
EXPOSE 8000
ENTRYPOINT mass_server run_uwsgi 
