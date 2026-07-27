# CCNA Automation Prep — Season 1, Episode 4: RESTCONF with Bruno & curl

This is **Episode 4 of Season 1** of a CCNA Automation prep series. Earlier
episodes made REST API calls to cloud controllers and looked at data formats.
This episode gets hands-on with **RESTCONF** — the HTTP-based protocol that lets
you read and write a device's configuration using **YANG data models** instead
of the CLI.

We drive the same set of calls two ways so you can see the request/response
cycle from both a GUI and the command line:

1. **[Bruno](https://www.usebruno.com/)** — an open-source API client. Import the
   included collection and click through the requests.
2. **`curl` + `jq`** — a set of shell scripts under [`scripts/`](./scripts) that
   make the identical RESTCONF calls from your terminal.

> **Maps to CCNA Automation exam topics 3.8, 5.10, and 5.11.** This episode goes
> well beyond what the exam asks of you — see
> [How this maps to the exam](#how-this-maps-to-the-exam) below for what you're
> actually expected to know.

---

## How this maps to the exam

This episode is deliberately **deeper than the CCNA Automation (200-901
CCNAAUTO) exam requires.** We construct payloads, navigate YANG paths, and call
RPCs so you build real intuition — but the exam does **not** expect you to do
any of that from memory. Read this section to calibrate what to *learn* versus
what's here just to *build understanding*.

The relevant exam topics ([official 200-901 CCNAAUTO topics, PDF](https://learningcontent.cisco.com/documents/marketing/exam-topics/200-901-CCNAAUTO_v.1.1.pdf)):

| Topic | Wording | What you're expected to do |
|-------|---------|----------------------------|
| **3.8** | *Apply concepts of model-driven programmability in a Cisco environment* | **Be aware** of the model: config/state comes from YANG data models, exposed over transports like RESTCONF/NETCONF. Know *why* it exists and how it differs from CLI screen-scraping. |
| **5.10** | *Interpret the results of a RESTCONF query* | Given a RESTCONF **response**, read it — identify the resource, the fields, and what the returned JSON is telling you. |
| **5.11** | *Identify the components of a YANG model* | Recognize YANG building blocks (containers, leaves, lists, the model namespace) when you see them. |

### What's fair game vs. beyond scope

| You **are** expected to… | You are **not** expected to… |
|--------------------------|------------------------------|
| Recognize that RESTCONF is HTTP(S) + REST verbs over YANG-modeled data | Hand-construct RESTCONF URLs / YANG paths from scratch |
| Interpret a returned JSON payload and pick out meaningful fields | Author PUT/POST request bodies from memory |
| Know GET reads, and that write/RPC operations exist | Memorize which RPC saves the config, or its exact path |
| Recognize YANG components (containers, leaves, lists, namespaces) | Read or write a full YANG module |
| Understand the model flavors that exist — native (vendor-native), OpenConfig (vendor-neutral), and IETF (standards-body) | Recall specific native / OpenConfig / IETF path syntax |

**Bottom line:** aim to *read and reason about* RESTCONF/YANG. Treat the
payload-building and path-navigation in the rest of this episode as
understanding-builders, not memorization targets.

---

## The big idea: RESTCONF is REST over YANG

RESTCONF exposes a device's YANG-modeled config and state as a REST API:

| REST concept | RESTCONF meaning |
|--------------|------------------|
| **URL path** | A path into the YANG data tree (e.g. `.../interface/Loopback=100`) |
| **GET** | Read config/state |
| **PUT** | Create or replace a resource (idempotent) |
| **POST** | Create a resource, or invoke an RPC/"operation" |
| **Media type** | `application/yang-data+json` (JSON) or `application/yang-data+xml` (XML) |

### JSON or XML — your choice

RESTCONF can encode the same YANG data as either **JSON** or **XML**. You pick
the encoding with the HTTP headers:

- **`Accept:`** tells the device which format you want *back* (the response).
- **`Content-Type:`** tells the device which format the body you're *sending*
  is in (for PUT/POST).

| Encoding | Media type |
|----------|------------|
| **JSON** | `application/yang-data+json` |
| **XML** | `application/yang-data+xml` |

This episode uses JSON throughout the scripts, but the choice is yours —
swapping those headers (and sending an XML body on writes) is fully valid in
both Bruno and the curl calls. The Bruno collection demonstrates the XML
variant live.

The same interface can be addressed through **two different YANG models**, and
this episode shows both side by side:

| Model | Example path | Flavor |
|-------|--------------|--------|
| **OpenConfig** | `openconfig-interfaces:interfaces/interface=GigabitEthernet1` | Vendor-neutral |
| **IOS-XE native** | `Cisco-IOS-XE-native:native/interface/GigabitEthernet=1` | Vendor-native |

---

## Lab target

You need a RESTCONF-capable Cisco IOS-XE device reachable over HTTPS. Pick
whichever of these fits you:

### Option 1 — DevNet always-on sandbox (no install)

Cisco hosts a free, shared **Catalyst 8000v always-on** sandbox you can use
without spinning up any infrastructure:

- **Catalog page:** [Cat8k Always-On sandbox](https://devnetsandbox.cisco.com/DevNet/catalog/Cat8k-Always-On_cat8k-always-on)
- **Host:** `devnetsandboxiosxec8k.cisco.com`
- **Port:** `443`

Log in on the catalog page to reserve/spin up the sandbox — it generates a
**unique username/password for your session**, so grab those credentials from
the sandbox details and use them below.

### Option 2 — Run your own (Catalyst 8000v or CSR1000v)

Run a **Catalyst 8000v** or **CSR1000v** yourself, e.g. in
[Cisco Modeling Labs (CML)](https://www.cisco.com/go/cml) — Personal, Personal
Plus, or Enterprise. Point the scripts/collection at that device's own address
and credentials.

> **Heads-up on free CML:** the free tier of CML does **not** ship with a
> RESTCONF-capable platform (no Catalyst 8000v or CSR1000v node images), so it
> can't run this lab. If you're on free CML, use the DevNet sandbox above.

### Connection details

Whichever path you pick, you'll plug four values — host, port, username,
password — into the scripts or the Bruno environment. This README uses
placeholders for them:

| Setting | Placeholder |
|---------|-------------|
| Host | `<HOST>` (e.g. `devnetsandboxiosxec8k.cisco.com`) |
| Port | `<PORT>` (typically `443`) |
| Username | `<USERNAME>` |
| Password | `<PASSWORD>` |

> **Heads-up:** RESTCONF must be enabled on the device
> (`restconf` / `ip http secure-server` in IOS-XE config) and the account needs
> privilege level 15. Sandboxes and lab devices typically use a self-signed
> cert, so the curl scripts pass `-k` to skip TLS verification — appropriate
> for a lab, not for production.

---

## Option A — Bruno

1. Install [Bruno](https://www.usebruno.com/downloads).
2. **Import Collection** → select
   [`CCNAAUTO-Prep_S1E4_RESTCONF.json`](./CCNAAUTO-Prep_S1E4_RESTCONF.json).
3. Select the **NetAcad RESTCONF Lab** environment (top-right) and fill in the
   host, port, username, and password for your device (see
   [Connection details](#connection-details)).
4. Work through the folders in order (01 → 06).

Auth is **Basic** at the collection root and inherited by every request, so the
username/password from the environment apply automatically.

---

## Option B — curl + jq

The [`scripts/`](./scripts) directory contains one script per Bruno folder. Each
makes the same RESTCONF call(s) with `curl` and pretty-prints the JSON with
[`jq`](https://jqlang.github.io/jq/).

> **You don't need to learn `jq`.** It isn't a RESTCONF or exam topic — we use
> it purely to pretty-print (and occasionally pick apart) the JSON that a
> RESTCONF call returns, so the output is readable. The interesting part is the
> `curl` request and the JSON response; `jq` is just the formatter.

### Prerequisites

| Tool | Why | Install |
|------|-----|---------|
| `curl` | Makes the HTTPS requests | Preinstalled on macOS/Linux |
| `jq` | Pretty-prints / filters JSON responses | `brew install jq` / `apt install jq` |

### Setting the connection variables

Each script sets the host, port, username, and password in a few plain
variables at the top. Edit those four lines to point at your device (the
DevNet sandbox or your own 8000v/CSR1000v — see
[Connection details](#connection-details)):

```bash
HOST="devnetsandboxiosxec8k.cisco.com"
PORT="443"
USER="<USERNAME>"
PASS="<PASSWORD>"
```

If you'd rather not touch the files, each variable also honors a matching
environment variable (`RESTCONF_HOST`, `RESTCONF_PORT`, `RESTCONF_USER`,
`RESTCONF_PASS`) — export those and they win over the defaults:

```bash
export RESTCONF_HOST="devnetsandboxiosxec8k.cisco.com"
export RESTCONF_PORT="443"
export RESTCONF_USER="<USERNAME>"
export RESTCONF_PASS="<PASSWORD>"
```

Or copy the provided [`scripts/.env.example`](./scripts/.env.example) and load
it into your shell:

```bash
cd scripts
cp .env.example .env
set -a; source .env; set +a
```

### Running

```bash
cd scripts

./01-get-device-config.sh              # full running config (native model)
./02-get-physical-interface-info.sh    # GE1 via OpenConfig + native
./03-get-loopback-config.sh            # read loopbacks (before)
./04-create-loopback-interface.sh      # PUT Loopback100 + Loopback101
./05-validate-created-loopbacks.sh     # read loopbacks (after)
./06-save-running-config.sh            # write mem via cisco-ia:save-config RPC
```

A typical demo runs `03` → `04` → `05` to show the loopbacks appear after the
`PUT`, then `06` to persist the change.

> **On the shared DevNet sandbox:** it's a shared, always-on device, so the
> write calls behave differently than on your own box:
> - **`04-create-loopback-interface.sh`** may return an error if someone else
>   already created `Loopback100`/`Loopback101`. That's expected — the resource
>   already exists. Either treat the error as "already done" and move on, or
>   change the loopback numbers in the script to unused ones.
> - **Skip `06-save-running-config.sh`** on the sandbox. Don't run the
>   `cisco-ia:save-config` RPC against a shared device — leave the running
>   config unsaved and let it reset. Only use `06` on a device you own.

### How the scripts are organized

Each script is fully self-contained — no shared library, no sourcing, no
helper functions. Every script sets its four connection variables at the top
and then issues one raw `curl` command per RESTCONF call, so you can read a
script top-to-bottom and see exactly what goes over the wire.

Each `curl` call sends the same handful of flags:

```bash
curl -sS -k \
  -u "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X GET \
  "https://${HOST}:${PORT}/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=100" | jq .
```

| Flag | Why |
|------|-----|
| `-sS` | Silent, but still show errors |
| `-k` | Skip TLS verification (self-signed lab cert) |
| `-u user:pass` | HTTP Basic auth |
| `-H "Accept: ..."` / `-H "Content-Type: ..."` | RESTCONF media type — `Accept` sets the response encoding, `Content-Type` the request-body encoding |
| `-X` | HTTP method (`GET` / `PUT` / `POST`) |
| `-d '{...}'` | JSON request body (PUT/POST only) |

These scripts request JSON, but you could swap both header values to
`application/yang-data+xml` to get (and send) XML instead — see
[JSON or XML — your choice](#json-or-xml--your-choice). If you switch to XML on
a write, the `-d` body must be XML too.

GET responses are piped through `jq` to pretty-print the JSON. PUT and POST
often return an empty body on success (HTTP 201/204), so those calls are left
un-piped — no output means the request succeeded.

---

## Endpoint reference

Every call below exists in **both** the Bruno collection and the scripts.

| # | Method | Path (under `/restconf`) | What it does |
|---|--------|--------------------------|--------------|
| 01 | GET | `/data/Cisco-IOS-XE-native:native/` | Whole running config |
| 02 | GET | `/data/openconfig-interfaces:interfaces/interface=GigabitEthernet1` | GE1 (OpenConfig) |
| 02 | GET | `/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=1` | GE1 (native) |
| 02 | GET | `/data/openconfig-interfaces:interfaces/interface=GigabitEthernet1/config/description` | GE1 description (OpenConfig) |
| 02 | GET | `/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=1/description` | GE1 description (native) |
| 03 | GET | `/data/openconfig-interfaces:interfaces/interface=Loopback101` | Loopback101 (OpenConfig) |
| 03 | GET | `/data/Cisco-IOS-XE-native:native/interface/Loopback=100` | Loopback100 (native) |
| 04 | PUT | `/data/openconfig-interfaces:interfaces/interface=Loopback101` | Create Loopback101 (OpenConfig) |
| 04 | PUT | `/data/Cisco-IOS-XE-native:native/interface/Loopback=100` | Create Loopback100 (native) |
| 05 | GET | `/data/Cisco-IOS-XE-native:native/interface/Loopback=100` | Validate Loopback100 |
| 05 | GET | `/data/openconfig-interfaces:interfaces/interface=Loopback101` | Validate Loopback101 |
| 06 | POST | `/operations/cisco-ia:save-config` | Save running → startup |
