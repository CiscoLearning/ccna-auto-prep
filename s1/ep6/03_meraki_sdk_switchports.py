#!/usr/bin/env python3
"""Demo 3: List switch ports with the Meraki Python SDK.

Demo 2 built every URL and header by hand. The SDK does that for you: you call
a Python method, and it handles the URL, the API key header, pagination, and
turning the JSON into Python objects.

Needs in .env:
    MERAKI_API_KEY   your Meraki Dashboard API key
    MERAKI_ORG_ID    the organization that has the switch

Run it:
    python3 03_meraki_sdk_switchports.py
"""

import os

import meraki
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("MERAKI_API_KEY")
ORG_ID = os.getenv("MERAKI_ORG_ID")

# One object gives you the whole Dashboard API.
# suppress_logging=True stops the SDK from printing and writing a log file.
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

# --- 1. Find the switches in the organization --------------------------------
# Same call as Demo 2 step 2, but as a method. productTypes filters to switches.
switches = dashboard.organizations.getOrganizationDevices(ORG_ID, productTypes=["switch"])

# --- 2. List the ports on each switch ----------------------------------------
for switch in switches:
    print(f"=== {switch['name']} ({switch['model']}, {switch['serial']}) ===")

    ports = dashboard.switch.getDeviceSwitchPorts(switch["serial"])

    print(f"  {'Port':<6} {'Name':<20} {'Enabled':<9} {'Type':<8} VLAN")
    for port in ports:
        print(f"  {port['portId']:<6} {str(port['name']):<20} {str(port['enabled']):<9} {port['type']:<8} {port['vlan']}")
    print()
