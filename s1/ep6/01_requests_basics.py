#!/usr/bin/env python3
"""Demo 1: Your first API calls with the requests library.

These are the same Deck of Cards calls from Season 1, Episode 1 (deck/*.sh),
rewritten in Python. The API is free and needs no key, so you can focus on the
three parts of every call: the request you build, the status code you get back,
and the JSON body you turn into Python objects.

Run it:
    python3 01_requests_basics.py
"""

import json

import requests

BASE_URL = "https://deckofcardsapi.com/api/deck"

# --- 1. GET: read something --------------------------------------------------
# requests.get() sends the HTTP request and hands back a Response object.
response = requests.get(f"{BASE_URL}/new/shuffle/")

print("=== 1. GET a new shuffled deck ===")
print("Status code: ", response.status_code)
print("Content-Type:", response.headers["Content-Type"])

# The body arrives as plain text: a string that happens to look like JSON.
print("Raw text:    ", response.text)
print("Type:        ", type(response.text))
print()

# json.loads() parses that JSON text into a Python dictionary.
deck = json.loads(response.text)
print("Type:        ", type(deck))

# response.json() is a shortcut that does the same json.loads() for you.
print("Same result? ", deck == response.json())

# json.dumps() goes the other way: dictionary -> JSON text, indented to read.
print(json.dumps(deck, indent=2))
print()

# Pull one value out by its key.
deck_id = deck["deck_id"]
print("Deck ID:     ", deck_id)

# Loop through the whole dictionary. .items() gives you each key and its value.
for key, value in deck.items():
    print(f"  {key:<10} = {value}")
print()

# --- 2. GET with a path parameter and a query parameter ----------------------
# The deck_id goes in the URL path. params= builds the "?count=5" for you.
response = requests.get(f"{BASE_URL}/{deck_id}/draw/", params={"count": 5})
data = response.json()

print("=== 2. GET: draw 5 cards ===")
print("Status code:", response.status_code)
print("Full URL:   ", response.url)

# data["cards"] is a list, and each card in it is a dictionary.
# Loop through the list, then pull values out of each card by key.
for card in data["cards"]:
    print(" ", card["value"], "of", card["suit"])
print("Cards left: ", data["remaining"])
print()

# --- 3. POST: change something -----------------------------------------------
# POST changes state on the server. Here it puts the cards back and reshuffles.
response = requests.post(f"{BASE_URL}/{deck_id}/shuffle/")
data = response.json()

print("=== 3. POST: reshuffle the deck ===")
print("Status code:", response.status_code)
print("Cards left: ", data["remaining"])
print()

# --- 4. When the call fails --------------------------------------------------
# requests does not raise an error on a 4xx/5xx. Always check the status code.
response = requests.get(f"{BASE_URL}/THISDECKDOESNOTEXIST/draw/")

print("=== 4. GET a deck that does not exist ===")
print("Status code:", response.status_code)
if response.status_code == 200:
    print("It worked!")
else:
    print("Something went wrong:", response.text)
