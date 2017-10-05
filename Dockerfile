FROM alpine:latest

# Install dependencies
RUN apk --no-cache add python3 python3-dev libffi libffi-dev libmagic tzdata git build-base automake autoconf libtool linux-headers

# Set timezone
RUN cp /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

# Install MASS server
RUN BUILD_LIB=1 pip3 install mass-server

# Create MASS user
RUN adduser -D mass
USER mass
WORKDIR /home/mass

# Add wsgi callable
ADD wsgi.py /home/mass/wsgi.py

# Run uwsgi
EXPOSE 8000
ENTRYPOINT uwsgi --module wsgi --callable app --http-socket :8000 --master --workers 5 --lazy-apps --enable-threads
