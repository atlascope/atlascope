#!/bin/sh

# Exit on errors.
set -e

# Test nginx configuration. Error if invalid.
nginx -t -q

# Start nginx in background, but attached to shell
# so that nginx exits when the shell exits.
# Process supervision is deemed unnecessary since
# the configuration is known to be good.
nginx &

# Execute provided command.
exec "$@"
