#!/usr/bin/env bash
#
# 06 - Save Running Config to Startup
#
# Invokes the cisco-ia:save-config RPC (a RESTCONF "operation") to persist the
# running configuration to startup - the API equivalent of "write memory".
# The body is an empty JSON object, matching the Bruno request.

# --- Connection details (edit these, or export them in your shell) ----------
HOST="${RESTCONF_HOST:-devnetsandboxiosxec8k.cisco.com}"
PORT="${RESTCONF_PORT:-443}"
USER="${RESTCONF_USER:-<USERNAME>}"
PASS="${RESTCONF_PASS:-<PASSWORD>}"

echo "### Save Config (running -> startup) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X POST \
  "https://${HOST}:${PORT}/restconf/operations/cisco-ia:save-config" \
  -d '{}'
