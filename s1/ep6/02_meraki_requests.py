#!/usr/bin/env python3
"""Demo 2: Call an authenticated API (Meraki Dashboard) with requests.

Same requests library as Demo 1, plus the one new thing: an API key sent in
the Authorization header. The key lives in the .env file, never in the script.

Needs in .env:
    MERAKI_API_KEY   your Meraki Dashboard API key
    MERAKI_ORG_ID    the organization to list devices from (step 1 prints its ID)

Run it:
    python3 02_meraki_requests.py
"""

import os

import requests
from dotenv import load_dotenv

# load_dotenv() reads .env and puts each line into the environment.
# os.getenv() then reads a value back out by name.
load_dotenv()
API_KEY = os.getenv("MERAKI_API_KEY")
ORG_ID = os.getenv("MERAKI_ORG_ID")

BASE_URL = "https://api.meraki.com/api/v1"

# The org we care about. Change this to your own org's name.
ORG_NAME = "Cisco U."

# Every Meraki call carries the API key as a Bearer token.
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
}

# --- 1. List the organizations this key can see ------------------------------
response = requests.get(f"{BASE_URL}/organizations", headers=headers)

print("=== 1. GET /organizations ===")
print("Status code:", response.status_code)
skipped = 0
for org in response.json():
    # .strip() removes any stray spaces around the name before comparing.
    if org["name"].strip() == ORG_NAME:
        print(f"  Found: {org['id']:<20} {org['name']}")
    else:
        skipped += 1
print("Skipped", skipped, "other orgs")
print()

# --- 2. List every device in one organization --------------------------------
response = requests.get(f"{BASE_URL}/organizations/{ORG_ID}/devices", headers=headers)
devices = response.json()

print(f"=== 2. GET /organizations/{ORG_ID}/devices ===")
print("Status code:", response.status_code)
print(f"  {'Name':<35} {'Model':<10} {'Serial':<16} Type")
for device in devices:
    print(f"  {device['name']:<35} {device['model']:<10} {device['serial']:<16} {device['productType']}")
print("Devices found:", len(devices))
print()

# --- 3. What a bad API key looks like ----------------------------------------
bad_headers = {"Authorization": "Bearer not-a-real-key"}
response = requests.get(f"{BASE_URL}/organizations", headers=bad_headers)

print("=== 3. GET /organizations with a bad key ===")
print("Status code:", response.status_code)
print("Body:       ", response.text)
