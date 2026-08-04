# Season 1, Episode 4 — RESTCONF & YANG: Practice Questions

These questions accompany the Episode 4 presentation and map to CCNA Automation
(200-901 **CCNAAUTO**) exam topics **3.8**, **5.10**, and **5.11**. They are
calibrated to what the exam actually expects — *recognizing* and *interpreting*
RESTCONF/YANG concepts — rather than hand-constructing paths or authoring
payloads from memory.

> Each question is followed by a collapsible **Answer** block containing the
> correct choice and a rationale. Try the question first, then expand it.

---

## Question 1 — What RESTCONF actually is

*(Exam topic 3.8 — model-driven programmability)*

Which statement **best** describes RESTCONF?

- **A.** A binary, connection-oriented protocol running over TCP port 830 that
  encodes all data as XML only.
- **B.** A CLI-scraping library that logs into the device over SSH and parses
  `show` command output into structured data.
- **C.** An HTTP(S)-based protocol that uses REST verbs (GET/PUT/POST/DELETE) to
  read and write a device's YANG-modeled configuration and operational state.
- **D.** A Cisco-proprietary replacement for SNMP that works exclusively with the
  IOS-XE native data model.

<details>
<summary>Answer</summary>

**Correct answer: C**

RESTCONF is REST over YANG: it rides on HTTP(S) and maps familiar REST verbs
onto operations against a device's YANG data tree — `GET` reads config/state,
`PUT`/`POST` create or replace resources, and `POST` also invokes RPCs.

- **A** describes **NETCONF** (TCP 830, XML), not RESTCONF. RESTCONF runs over
  HTTPS (typically 443) and supports **both JSON and XML** encodings.
- **B** describes screen-scraping — the *opposite* of model-driven
  programmability. RESTCONF returns structured, model-defined data, not parsed
  CLI text.
- **D** is wrong on two counts: RESTCONF is an **IETF standard** (RFC 8040), not
  Cisco-proprietary, and it works with multiple model flavors (native,
  OpenConfig, IETF) — not just IOS-XE native.

</details>

---

## Question 2 — Interpreting a RESTCONF query

*(Exam topic 5.10 — interpret the results of a RESTCONF query)*

You run the following request against an IOS-XE device:

```bash
curl -sS -k -u user:pass \
  -H "Accept: application/yang-data+json" \
  -X GET \
  "https://<HOST>:443/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=100"
```

The device returns:

```json
{
  "Cisco-IOS-XE-native:Loopback": {
    "name": 100,
    "description": "Configured via RESTCONF",
    "ip": {
      "address": {
        "primary": {
          "address": "10.0.0.100",
          "mask": "255.255.255.255"
        }
      }
    }
  }
}
```

What is this response telling you?

- **A.** Loopback100 currently exists and is configured with the description
  "Configured via RESTCONF" and IP address 10.0.0.100/32.
- **B.** The request failed; the device is reporting that Loopback100 does not
  exist.
- **C.** The device just created Loopback100 as a result of this call.
- **D.** The response is operational (state) data showing live interface
  counters for Loopback100.

<details>
<summary>Answer</summary>

**Correct answer: A**

This is a `GET` — a **read**. The returned JSON is the configuration data for
`Loopback=100`: its `name` (100), its `description`, and its IPv4 `address`
(10.0.0.100 with a `255.255.255.255` / `/32` mask). Reading those fields out of
the payload is exactly what topic 5.10 asks you to do.

- **B** is wrong — a populated body was returned. A nonexistent resource would
  typically return an HTTP 404 with an error payload, not this data.
- **C** is wrong — `GET` never creates anything. Creating/replacing a resource
  is `PUT` (or `POST`); a successful write usually returns an **empty body**
  (HTTP 201/204), not populated config.
- **D** is wrong — these are configuration leaves (description, IP address), not
  operational counters like packet/byte counts or interface up/down status.

</details>

---

## Question 3 — Identifying YANG model components

*(Exam topic 5.11 — identify the components of a YANG model)*

Look at this excerpt of RESTCONF-returned data:

```json
{
  "Cisco-IOS-XE-native:native": {
    "interface": {
      "Loopback": [
        { "name": 100, "description": "site-A" },
        { "name": 101, "description": "site-B" }
      ]
    }
  }
}
```

Which identification of the YANG building blocks is **correct**?

- **A.** `native` is a leaf, `interface` is a list, and `name` is a container.
- **B.** `Loopback` is a leaf-list, and `100`/`101` are containers.
- **C.** `description` is a list because it appears more than once.
- **D.** `Cisco-IOS-XE-native` is the module (namespace) prefix, `interface` is a
  container, `Loopback` is a list, and `name`/`description` are leaves.

<details>
<summary>Answer</summary>

**Correct answer: D**

Matching the JSON to YANG building blocks:

- `Cisco-IOS-XE-native` before the colon is the **module name / namespace
  prefix** — it tells you which YANG model this data comes from.
- `interface` groups related nodes and holds no value of its own → **container**.
- `Loopback` is a JSON **array** of entries, each uniquely keyed by `name` →
  **list** (a YANG list is the modeled construct behind that array).
- `name` and `description` hold a single scalar value each → **leaves**.

- **A** mislabels every element (`native` is a container, not a leaf; `name` is a
  leaf, not a container).
- **B** is wrong — `Loopback` holds multiple *complex objects* (a **list**), not
  a set of bare scalar values (which is what a **leaf-list** is).
- **C** is wrong — `description` is a single leaf that appears once *per list
  entry*; repetition across entries doesn't make it a list.

</details>

---

## Question 4 — Choosing the right verb

*(Exam topic 3.8 / 5.10 — read vs. write operations)*

During the demo you first read the loopback interfaces, then create a new one,
then read again to confirm it appeared. Which sequence of HTTP methods matches
that "read → create → confirm" flow?

- **A.** `POST` → `GET` → `POST`
- **B.** `GET` → `PUT` → `GET`
- **C.** `PUT` → `DELETE` → `PUT`
- **D.** `GET` → `GET` → `GET`

<details>
<summary>Answer</summary>

**Correct answer: B**

- **Read** the current loopbacks → `GET` (safe, returns data).
- **Create/replace** the new loopback resource → `PUT` (idempotent create-or-
  replace at a known path).
- **Confirm** it now exists → `GET` again.

This is exactly the `03 → 04 → 05` script flow in the episode.

- **A** uses `POST` to read, which is incorrect — reads are `GET`.
- **C** never reads and would delete rather than confirm.
- **D** never writes, so nothing would ever be created.

> Note: `POST` *can* create a resource too, but the episode's create step uses
> `PUT` against a specific resource path, which is the idempotent create-or-
> replace choice.

</details>

---

## Question 5 — JSON vs. XML and the media-type headers

*(Exam topic 3.8 / 5.10 — RESTCONF encodings and headers)*

A colleague's `GET` request keeps returning XML, but they want JSON back. They
are sending:

```
Accept: application/yang-data+xml
Content-Type: application/yang-data+json
```

Which change gets them a **JSON** response?

- **A.** Change `Content-Type` to `application/yang-data+xml`.
- **B.** Remove both headers — RESTCONF always defaults to JSON.
- **C.** Change `Accept` to `application/yang-data+json`.
- **D.** Add `-X JSON` to the request.

<details>
<summary>Answer</summary>

**Correct answer: C**

The **`Accept`** header tells the device which encoding you want *back* (the
response). It is currently set to `...+xml`, so the device honors that and
replies in XML. Switching `Accept` to `application/yang-data+json` returns JSON.

- **A** changes `Content-Type`, which describes the encoding of the **body you
  send** (relevant to `PUT`/`POST`), not the response — so it wouldn't change
  what comes back. On a bodiless `GET` it's irrelevant.
- **B** is wrong — there's no guaranteed universal default, and the whole point
  is that headers control the encoding. RESTCONF supports both JSON and XML.
- **D** is not a real thing — `-X` sets the HTTP **method** (GET/PUT/POST), not
  an encoding.

</details>

---

## Question 6 — YANG model flavors (multiple answer — pick 3)

*(Exam topic 5.11 / 3.8 — recognize the model flavors that exist)*

The episode addresses the **same** GigabitEthernet1 interface through more than
one YANG model. Which **three** of the following are legitimate categories
("flavors") of YANG data models? **(Choose three.)**

- **A.** OpenConfig — a vendor-neutral, industry-consortium model
- **B.** IETF — models published by the standards body (e.g. `ietf-interfaces`)
- **C.** Native — the vendor's own device-specific model (e.g.
  `Cisco-IOS-XE-native`)
- **D.** SNMP-MIB — a YANG flavor defined by SNMP management information bases
- **E.** RESTCONF — a YANG flavor that only exists when queried over HTTPS
- **F.** CLI-native — a YANG flavor generated by parsing `show run` output
- **G.** NETCONF — a YANG flavor tied to TCP port 830

<details>
<summary>Answer</summary>

**Correct answers: A, B, C**

There are three commonly cited YANG **model flavors**, and the episode names all
three:

- **A — OpenConfig:** vendor-neutral models from the OpenConfig consortium.
  Portable across vendors (e.g. `openconfig-interfaces`).
- **B — IETF:** models standardized by the IETF (e.g. `ietf-interfaces`,
  RFC-defined).
- **C — Native:** the vendor's own model that maps directly to that platform's
  features (e.g. `Cisco-IOS-XE-native`). Most complete for that box, least
  portable.

Why the others are wrong:

- **D — SNMP-MIB** is a different management framework (SMI/MIBs), not a YANG
  model flavor. (YANG *can* be derived from MIBs, but "SNMP-MIB flavor" is not a
  category you'd pick here.)
- **E — RESTCONF** and **G — NETCONF** are **transports/protocols** that *carry*
  YANG-modeled data — they are not model flavors themselves.
- **F — CLI-native** is invented; screen-scraping the CLI is the pre-model
  approach YANG replaces, not a YANG flavor.

**Key idea:** *transport* (RESTCONF/NETCONF) and *model flavor*
(native/OpenConfig/IETF) are independent choices — you can carry any flavor over
either transport.

</details>

---

### Exam-topic coverage summary

| Question | Focus | Correct | Topic(s) |
|----------|-------|---------|----------|
| 1 | What RESTCONF is (vs. NETCONF / screen-scraping) | C | 3.8 |
| 2 | Interpreting a returned JSON payload | A | 5.10 |
| 3 | Identifying YANG components (container/list/leaf/namespace) | D | 5.11 |
| 4 | Read vs. create vs. confirm (GET/PUT/GET) | B | 3.8, 5.10 |
| 5 | JSON vs. XML via `Accept`/`Content-Type` headers | C | 3.8, 5.10 |
| 6 | YANG model flavors — native / OpenConfig / IETF (pick 3) | A, B, C | 5.11, 3.8 |
