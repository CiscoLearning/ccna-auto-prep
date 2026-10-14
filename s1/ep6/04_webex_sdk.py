#!/usr/bin/env python3
"""Demo 4: Read your Webex rooms and post a message with the Webex Python SDK.

A bot only sees the rooms (spaces) it has been added to. Add your bot to a
space first, then put that space's exact title in WEBEX_ROOM_TITLE.

Needs in .env:
    WEBEX_BOT_TOKEN    your bot's access token (developer.webex.com)
    WEBEX_ROOM_TITLE   the title of the space to post into

Run it:
    python3 04_webex_sdk.py
"""

import os

from dotenv import load_dotenv
from webexpythonsdk import WebexAPI

load_dotenv()
BOT_TOKEN = os.getenv("WEBEX_BOT_TOKEN")
ROOM_TITLE = os.getenv("WEBEX_ROOM_TITLE")

# One object gives you the whole Webex API, authenticated with the bot token.
api = WebexAPI(access_token=BOT_TOKEN)

# --- 1. Who am I? ------------------------------------------------------------
me = api.people.me()
print("=== 1. Signed in as ===")
print(" ", me.displayName, f"({me.emails[0]})")
print()

# --- 2. List the rooms the bot is in -----------------------------------------
# The SDK returns objects, so you use dots (room.title), not room["title"].
print("=== 2. Rooms ===")
room_id = None
for room in api.rooms.list():
    print(f"  {room.title:<40} {room.type}")
    if room.title == ROOM_TITLE:
        room_id = room.id
print()

# --- 3. Post a message into one room -----------------------------------------
print(f"=== 3. Post a message to '{ROOM_TITLE}' ===")
message = api.messages.create(
    roomId=room_id,
    markdown="Hello from **Python**! Sent with the Webex SDK during CCNA Automation Prep, Episode 6.",
)
print("  Message sent at", message.created)
