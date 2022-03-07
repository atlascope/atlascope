FROM ubuntu:20.04

# Install system libraries for Python packages:
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --yes \
        nginx \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir /tiles

COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./red.png /tiles
COPY ./green.png /tiles
COPY ./blue.png /tiles
COPY ./yellow.png /tiles

COPY ./speckled-red.png /tiles
COPY ./speckled-green.png /tiles
COPY ./speckled-blue.png /tiles
COPY ./speckled-yellow.png /tiles

EXPOSE 9005
ENTRYPOINT ["nginx"]
