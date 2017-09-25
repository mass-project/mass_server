FROM eboraas/debian:latest

# Install dependencies
RUN apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get -y install python3 python3-pip python3-dev build-essential ssdeep libffi-dev autoconf automake libtool && \
    apt-get -y clean

# Install MASS server
RUN pip3 install mass-server

# Create MASS user
RUN useradd -m mass
WORKDIR /mass/mass_server

# Run uwsgi
USER mass
EXPOSE 8000
ENTRYPOINT uwsgi --module wsgi --callable app --http-socket :8000 --master --workers 5 --lazy-apps --enable-threads
