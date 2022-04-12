#!/bin/sh
mkdir -p /data
python -m simple_httpfs /data --schema=http
exec "$@"
