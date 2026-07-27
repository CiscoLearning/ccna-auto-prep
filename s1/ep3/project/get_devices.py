#!/usr/bin/env python3
"""Read a list of Meraki devices from devices.json and print a styled table.

This is a stand-in for the live Meraki Dashboard API call from Season 1,
Episode 1 (meraki/13_get_devices.sh). Instead of hitting the network, it reads
the same shape of data from a local file so it runs anywhere -- no API key, no
account, no internet. That makes it perfect content to practice Git on.

Install Rich first:
    pip install rich

Run it:
    python3 get_devices.py
"""

import json

from rich.console import Console
from rich.table import Table

# Load the device inventory from disk. json.load turns the JSON text into
# Python objects: the top level becomes a dict, "devices" becomes a list.
with open("devices.json") as f:
    data = json.load(f)

devices = data["devices"]

# Build a Rich table. This is the block you'll edit later to create a Git diff
# and a merge conflict -- keep an eye on the title and the columns.
table = Table(title=f"Meraki Devices ({len(devices)} found)")
table.add_column("Name", style="cyan", no_wrap=True)
table.add_column("Model", style="magenta")
table.add_column("Serial", style="green")
# table.add_column("LAN IP", style="yellow")

for device in devices:
    table.add_row(
        device["name"],
        device["model"],
        device["lanIp"],
    )

# Console().print renders the table with colors and borders to your terminal.
Console().print(table)
