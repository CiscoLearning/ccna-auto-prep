#!/usr/bin/env bash
#
# 03 - Get Loopback Configuration
#
# Reads the loopback interface through all three models before we create/modify
# it. Expect these to return 404-style errors if the loopbacks don't exist yet -
# run this before and after script 04 to see the difference.
#   - OpenConfig: Loopback101
#   - IOS-XE native: Loopback100
#   - IETF: Loopback102

# --- Connection details (edit these, or export them in your shell) ----------
HOST="${RESTCONF_HOST:-devnetsandboxiosxec8k.cisco.com}"
PORT="${RESTCONF_PORT:-443}"
USER="${RESTCONF_USER:-<USERNAME>}"
PASS="${RESTCONF_PASS:-<PASSWORD>}"

echo "### Get Loopback Config (OpenConfig - Loopback101) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X GET \
  "https://${HOST}:${PORT}/restconf/data/openconfig-interfaces:interfaces/interface=Loopback101" | jq .

echo
echo "### Get Loopback Config (IOS-XE native - Loopback100) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X GET \
  "https://${HOST}:${PORT}/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=100" | jq .

echo
echo "### Get Loopback Config (IETF - Loopback102) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X GET \
  "https://${HOST}:${PORT}/restconf/data/ietf-interfaces:interfaces/interface=Loopback102" | jq .
