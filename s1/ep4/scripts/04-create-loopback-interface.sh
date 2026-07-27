#!/usr/bin/env bash
#
# 04 - Create Loopback Interface
#
# Creates two loopback interfaces with PUT (idempotent create/replace):
#   - OpenConfig model  -> Loopback101 (192.0.3.101/32)
#   - IOS-XE native model -> Loopback100 (192.0.2.100/32)
#
# The JSON bodies are the same payloads carried by the Bruno collection.

# --- Connection details (edit these, or export them in your shell) ----------
HOST="${RESTCONF_HOST:-devnetsandboxiosxec8k.cisco.com}"
PORT="${RESTCONF_PORT:-443}"
USER="${RESTCONF_USER:-<USERNAME>}"
PASS="${RESTCONF_PASS:-<PASSWORD>}"

echo "### Create Loopback Interface (OpenConfig - Loopback101) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X PUT \
  "https://${HOST}:${PORT}/restconf/data/openconfig-interfaces:interfaces/interface=Loopback101" \
  -d '{
  "openconfig-interfaces:interface": [
    {
      "name": "Loopback101",
      "config": {
        "name": "Loopback101",
        "type": "iana-if-type:softwareLoopback",
        "enabled": true,
        "description": "Configured via RESTCONF and OpenConfig models"
      },
      "subinterfaces": {
        "subinterface": [
          {
            "index": 0,
            "config": {
              "index": 0,
              "enabled": true,
              "description": "Configured via RESTCONF and OpenConfig models"
            },
            "openconfig-if-ip:ipv4": {
              "addresses": {
                "address": [
                  {
                    "ip": "192.0.3.101",
                    "config": {
                      "ip": "192.0.3.101",
                      "prefix-length": 32
                    }
                  }
                ]
              }
            }
          }
        ]
      }
    }
  ]
}'

echo
echo "### Create Loopback Interface (IOS-XE native - Loopback100) ###"
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X PUT \
  "https://${HOST}:${PORT}/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=100" \
  -d '{
  "Cisco-IOS-XE-native:Loopback": [
    {
      "name": 100,
      "description": "Created via RESTCONF",
      "ip": {
        "address": {
          "primary": {
            "address": "192.0.2.100",
            "mask": "255.255.255.255"
          }
        }
      }
    }
  ]
}'
