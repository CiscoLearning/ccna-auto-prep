# CCNA Automation Prep — Season 1, Episode 6: Python, requests & SDKs

This is **Episode 6 of Season 1** of a CCNA Automation prep series. Episode 1
made REST calls with `curl`. This episode makes the same kind of calls from
**Python**, first with the `requests` library and then with vendor **SDKs**
that wrap the API for you.

There are four live demos, all at the same level and run in this order:

1. **`requests` basics.** The Deck of Cards API from Episode 1, with no key
   needed. GET, POST, status codes, and turning JSON into Python.
2. **Meraki with `requests`.** The same mechanics against an authenticated API.
   The API key comes from a `.env` file and goes in a `Bearer` header.
3. **Meraki with the SDK.** The same API key, but the
   [Meraki Python SDK](https://github.com/meraki/dashboard-api-python) builds
   the calls. Lists the ports on every switch in the org.
4. **Webex with the SDK.** The
   [Webex Python SDK](https://github.com/WebexCommunity/WebexPythonSDK) lists
   the rooms a bot is in and posts a message into one.

> **Maps to CCNA Automation exam topics 2.1–2.7, 3.1, 3.9.b, 4.8, and 5.2.** See
> the official
> [200-901 CCNAAUTO exam topics (PDF)](https://learningcontent.cisco.com/documents/marketing/exam-topics/200-901-CCNAAUTO_v.1.1.pdf).

---

## How this maps to the exam

| Topic | What you're expected to do | Demo |
|-------|----------------------------|------|
| **1.2** | Parse JSON into Python and pull values out of dictionaries and lists | 1 |
| **2.1** | Build a request: the URL, the verb (GET/POST), path and query parameters | 1, 2 |
| **2.3–2.5** | Read a status code and know what a 4xx means. Don't assume a call worked | 1, 2 |
| **2.6** | Know the parts of a response: status code, headers, body | 1 |
| **2.7** | Authenticate with an API key or token in a header | 2, 4 |
| **3.1, 5.2** | Recognize what an SDK gives you over raw `requests` | 2 vs. 3 |
| **3.9.b** | Recognize Webex API objects: rooms (spaces), messages, people | 4 |
| **4.8** | Keep secrets out of your code (`.env` + `os.getenv`) | 2, 3, 4 |

**Bottom line:** most Python objectives ask you to **read** code and say what
it does, not write it from memory. The scripts are short and run top to bottom
so you can practice exactly that.

> The scripts are intentionally kept at CCNA-Automation level: no functions,
> classes, or argument parsing, and no defensive checks. If a key is wrong
> you'll see the API's real error, which is itself a useful teaching moment.

---

## The big idea: `requests` vs. an SDK

Demos 2 and 3 talk to the **same Meraki API with the same key**. The difference
is who builds the HTTP call.

```python
# Demo 2: you build the URL and headers yourself
headers = {"Authorization": f"Bearer {API_KEY}"}
url = f"{BASE_URL}/organizations/{ORG_ID}/devices"
devices = requests.get(url, headers=headers).json()

# Demo 3: the SDK builds them for you
dashboard = meraki.DashboardAPI(API_KEY)
devices = dashboard.organizations.getOrganizationDevices(ORG_ID)
```

Both return the same list of devices. The SDK also handles pagination and rate
limiting (HTTP 429) for you. The Webex SDK goes one step further and returns
objects, so you write `room.title` instead of `room["title"]`.

---

## Prerequisites

| Tool | Why | Install (macOS) |
|------|-----|-----------------|
| Python 3.10+ | Runs the scripts | `brew install python` |
| The packages in [`requirements.txt`](./requirements.txt) | `requests`, `python-dotenv`, `meraki`, `webexpythonsdk` | See [Setup](#setup) |

**For Demos 2 and 3 (Meraki):**

- A **Meraki Dashboard account** with API access enabled
  (Dashboard → *Organization → Settings → Enable API access*).
- A **Meraki API key** (Dashboard → *My Profile → API access → Generate key*).
- An org that has at least one **MS switch** for Demo 3.

**For Demo 4 (Webex):**

- A **Webex bot**: [developer.webex.com](https://developer.webex.com) →
  *My Webex Apps → Create a Bot*. Copy the bot's access token.
- A **space with the bot added to it.** A bot only sees spaces it has been
  added to. Put the space's exact title in `WEBEX_ROOM_TITLE`.

---

## Setup

```bash
cd s1/ep6

# A virtual environment keeps these packages out of your system Python
python3 -m venv .venv
source .venv/bin/activate          # fish: source .venv/bin/activate.fish
pip install -r requirements.txt

# Your credentials go in .env (already in .gitignore, never commit it)
cp .env.example .env
```

Then open `.env` and fill in:

| Variable | Used by | Where to get it |
|----------|---------|-----------------|
| `MERAKI_API_KEY` | 02, 03 | Meraki Dashboard → *My Profile → API access* |
| `MERAKI_ORG_ID` | 02, 03 | Set `ORG_NAME` in `02_meraki_requests.py` and run it once; step 1 prints that org's ID |
| `WEBEX_BOT_TOKEN` | 04 | developer.webex.com → your bot |
| `WEBEX_ROOM_TITLE` | 04 | The title of a space your bot is in |

Each script calls `load_dotenv()` to read `.env`, so there's nothing to
`export` or `source`.

---

## Files in this directory

| File | Summary |
|------|---------|
| [`00_venv.md`](./00_venv.md) | The three commands to build and activate a virtual environment and install `requirements.txt`. Run these first. |
| [`01_requests_basics.py`](./01_requests_basics.py) | GET a new deck and parse the JSON text into a dictionary (`json.loads` / `json.dumps`), loop through a dictionary and a list of dictionaries, GET with path + query parameters, POST to reshuffle, and a deliberate **404**. |
| [`02_meraki_requests.py`](./02_meraki_requests.py) | Loops over the orgs your key can see and uses an `if`/`else` to print only `ORG_NAME`, then lists every device in `MERAKI_ORG_ID`. Ends with a bad key so you see a **401**. |
| [`03_meraki_sdk_switchports.py`](./03_meraki_sdk_switchports.py) | Uses `meraki.DashboardAPI` to find the switches in the org and list each one's ports: port ID, name, enabled, type, VLAN. |
| [`04_webex_sdk.py`](./04_webex_sdk.py) | Uses `WebexAPI` to show who the bot is, list its rooms, and post a markdown message into `WEBEX_ROOM_TITLE`. |
| [`requirements.txt`](./requirements.txt) | The four packages the demos need. |
| [`.env.example`](./.env.example) | Template for your `.env`. Copy it and fill in your own values. |

---

## Running the demos

```bash
python3 01_requests_basics.py         # no key needed
python3 02_meraki_requests.py         # needs MERAKI_API_KEY + MERAKI_ORG_ID
python3 03_meraki_sdk_switchports.py  # same Meraki values
python3 04_webex_sdk.py               # needs WEBEX_BOT_TOKEN + WEBEX_ROOM_TITLE
```

### Things to try live

- **Demo 1:** change `params={"count": 5}` to `{"count": 60}`. The status is
  still **200**, but the body says `"success": false` with an error. A 200 only
  means the server handled the request. Read the body too.
- **Demo 2:** compare step 2's table with Episode 1's
  `meraki/13_get_devices.sh`. It's the same API call, made from curl vs. Python.
- **Demo 3:** add `print(ports[0])` inside the loop to see the full dictionary
  the SDK returns for one port. The table only shows five of its fields.
- **Demo 4:** set `WEBEX_ROOM_TITLE` to a space the bot is **not** in. The
  message call fails because `room_id` is still `None`. That's a good reason
  to read an error message carefully.
