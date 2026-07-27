#!/usr/bin/env bash
#
# 01 - Get Device Config
#
# Retrieves the entire Cisco-IOS-XE-native running configuration from the
# device (the top-level "native" container). This is a large payload, so the
# jq output is a good place to explore what the device exposes over RESTCONF.

# --- Connection details (edit these, or export them in your shell) ----------
HOST="${RESTCONF_HOST:-devnetsandboxiosxec8k.cisco.com}"
PORT="${RESTCONF_PORT:-443}"
USER="${RESTCONF_USER:-<USERNAME>}"
PASS="${RESTCONF_PASS:-<PASSWORD>}"

echo "### Get Device Config (Top Level) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X GET \
  "https://${HOST}:${PORT}/restconf/data/Cisco-IOS-XE-native:native/" | jq .
