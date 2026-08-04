#!/usr/bin/env bash
#
# 02 - Get Physical Interface Information
#
# Six GETs that show the same physical interface (GigabitEthernet1) through
# three different YANG models:
#   - openconfig-interfaces (vendor-neutral)
#   - Cisco-IOS-XE-native   (vendor-native)
#   - ietf-interfaces       (IETF standard)
# and then drills into just the interface description for each model.

# --- Connection details (edit these, or export them in your shell) ----------
HOST="${RESTCONF_HOST:-devnetsandboxiosxec8k.cisco.com}"
PORT="${RESTCONF_PORT:-443}"
USER="${RESTCONF_USER:-<USERNAME>}"
PASS="${RESTCONF_PASS:-<PASSWORD>}"

echo "### Get GE1 Config (OpenConfig) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X GET \
  "https://${HOST}:${PORT}/restconf/data/openconfig-interfaces:interfaces/interface=GigabitEthernet1" | jq .

echo
echo "### Get GE1 Config (IOS-XE native) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X GET \
  "https://${HOST}:${PORT}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=1" | jq .

echo
echo "### Get GE1 Config (IETF) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X GET \
  "https://${HOST}:${PORT}/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1" | jq .

echo
echo "### Get GE1 Description (OpenConfig) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X GET \
  "https://${HOST}:${PORT}/restconf/data/openconfig-interfaces:interfaces/interface=GigabitEthernet1/config/description" | jq .

echo
echo "### Get GE1 Description (IOS-XE native) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X GET \
  "https://${HOST}:${PORT}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=1/description" | jq .

echo
echo "### Get GE1 Description (IETF) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X GET \
  "https://${HOST}:${PORT}/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1/description" | jq .
