#!/bin/sh
set -eu

: "${GOOGLE_MAPS_API_KEY:=}"
# API keys contain only these characters; reject script injection in runtime config.
case "$GOOGLE_MAPS_API_KEY" in
  *[!A-Za-z0-9_-]*)
    printf '%s\n' 'Invalid characters in GOOGLE_MAPS_API_KEY' >&2
    exit 1
    ;;
esac
printf 'window.IOT_CONFIG = {googleMapsApiKey: "%s"};\n' "$GOOGLE_MAPS_API_KEY" \
  > /usr/local/apache2/htdocs/runtime-config.js
exec "$@"
