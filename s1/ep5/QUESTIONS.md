# Season 1, Episode 5 — NETCONF & YANG: Practice Questions

These questions accompany the Episode 5 presentation and map to CCNA Automation
(200-901 **CCNAAUTO** v1.1) exam topics **3.8**, **5.10**, and **5.11**, with a
couple that touch **6.7** (protocol ports) and **5.3** (network simulation
tools). They're calibrated to what the exam expects — *recognizing* and
*interpreting* NETCONF/YANG concepts and reading a YANG tree — not
hand-authoring RPCs from memory.

> Each question is followed by a collapsible **Answer** block with the correct
> choice and a rationale. Try the question first, then expand it.

---

## Question 1 — What NETCONF actually is

*(Exam topic 3.8 — model-driven programmability)*

Which statement **best** describes NETCONF?

- **A.** A REST API that uses GET/PUT/POST verbs over HTTPS to act on
  YANG-modeled data, encoding it as JSON or XML.
- **B.** An XML-based protocol that runs over SSH (TCP 830) and uses RPC
  operations like `<get-config>` and `<edit-config>` to read and write a
  device's YANG-modeled configuration.
- **C.** A CLI-automation library that opens an SSH session and scrapes the
  output of `show` commands into structured data.
- **D.** A Cisco-proprietary telemetry protocol that streams operational
  counters and works only with the IOS-XE native model.

<details>
<summary>Answer</summary>

**Correct answer: B**

NETCONF (IETF **RFC 6241**) is an **XML-based, RPC-style** protocol that runs
over **SSH on TCP 830**. It carries **YANG-modeled** config/state and exposes
named operations — `<get-config>`, `<get>`, `<edit-config>`, `<commit>`, etc. —
plus explicit datastores (`running`, `candidate`, `startup`).

- **A** describes **RESTCONF** (RFC 8040) — HTTP(S), REST verbs, JSON *or* XML.
- **C** describes screen-scraping, the pre-model approach YANG replaces.
- **D** is wrong on both counts: NETCONF is an **IETF standard**, not Cisco
  proprietary, and it works with multiple model flavors (native, OpenConfig,
  IETF), not just IOS-XE native.

</details>

---

## Question 2 — NETCONF vs. RESTCONF

*(Exam topic 3.8 / 6.7 — transports and ports)*

Your teammate says "NETCONF and RESTCONF are the same thing." Which comparison
is **accurate**?

- **A.** NETCONF runs over SSH on **TCP 830** and encodes data as **XML**;
  RESTCONF runs over **HTTP(S)** and can encode as **JSON or XML**.
- **B.** NETCONF uses HTTP verbs; RESTCONF uses `<rpc>` operations.
- **C.** NETCONF is JSON-only; RESTCONF is XML-only.
- **D.** They use different data models — NETCONF requires OpenConfig and
  RESTCONF requires the native model.

<details>
<summary>Answer</summary>

**Correct answer: A**

The two protocols carry the **same** YANG-modeled data but differ on the wire:

- **NETCONF** — SSH, **TCP 830**, **XML only**, RPC-style operations, explicit
  datastores.
- **RESTCONF** — HTTP(S) (typically 443), **JSON or XML**, REST verbs.

- **B** swaps them — RESTCONF uses HTTP verbs; NETCONF uses `<rpc>` operations.
- **C** is backwards on encodings (NETCONF is XML; RESTCONF does both).
- **D** is wrong — **transport and model flavor are independent**. Any flavor
  (native / OpenConfig / IETF) can ride over either protocol.

</details>

---

## Question 3 — Interpreting a NETCONF reply

*(Exam topic 5.10 — interpret the results of a NETCONF query)*

You send a `<get-config>` and the device returns:

```xml
<rpc-reply message-id="103" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <interface>
        <Loopback>
          <name>100</name>
          <description>Configured via NETCONF</description>
          <ip>
            <address>
              <primary>
                <address>10.0.0.100</address>
                <mask>255.255.255.255</mask>
              </primary>
            </address>
          </ip>
        </Loopback>
      </interface>
    </native>
  </data>
</rpc-reply>
```

What is this reply telling you?

- **A.** The request failed; `<rpc-reply>` with `<data>` indicates an error.
- **B.** Loopback100 exists, described "Configured via NETCONF", with IP
  10.0.0.100/32.
- **C.** The device just created Loopback100 as a result of this call.
- **D.** These are live operational counters for Loopback100.

<details>
<summary>Answer</summary>

**Correct answer: B**

The `<data>` payload is the **configuration** returned by a read
(`<get-config>`). Reading it out: interface `Loopback` with key `<name>100`, a
`<description>`, and a primary IPv4 `<address>` of `10.0.0.100` with
`<mask>255.255.255.255</mask>` — a `/32`. That's exactly the interpretation
topic 5.10 asks for.

- **A** is wrong — a `<data>` block is a **successful** read. An error would
  come back as `<rpc-error>`.
- **C** is wrong — a read never creates anything; that's `<edit-config>`, which
  returns `<ok/>`, not populated data.
- **D** is wrong — these are configuration leaves (description, IP), not
  operational counters like packet/byte counts.

</details>

---

## Question 4 — Reading a YANG tree

*(Exam topic 5.11 — interpret basic YANG models)*

You're looking at an RFC 8340 tree for the native interface model:

```
module: Cisco-IOS-XE-native
  +--rw native
     +--rw interface
        +--rw Loopback* [name]
           +--rw name           uint32
           +--rw description?   string
```

Which identification of the building blocks is **correct**?

- **A.** `native` is a leaf, `interface` is a list, and `name` is a container.
- **B.** `Cisco-IOS-XE-native` is the namespace, `native` and `interface` are
  containers, `Loopback` is a **list** keyed by `name`, and `name`/`description`
  are **leaves**.
- **C.** `Loopback` is a leaf-list, and `name` is its key.
- **D.** `description` is required because every interface has one.

<details>
<summary>Answer</summary>

**Correct answer: B**

Reading the notation:

- `module: Cisco-IOS-XE-native` → the **namespace** (which model this is).
- `native` and `interface` → **containers** (branches that group nodes).
- `Loopback* [name]` → the `*` marks a **list** and `[name]` names its **key**.
- `name` and `description` → **leaves** (single values). The `?` on
  `description?` marks it **optional**.

- **A** mislabels everything.
- **C** is wrong — `Loopback` holds complex entries (a **list**), not bare
  scalars (which is what a **leaf-list** is). The `[name]` key confirms a list.
- **D** is wrong — the `?` on `description?` means it's **optional**, not
  required.

</details>

---

## Question 5 — choice / case in a YANG tree

*(Exam topic 5.11 — interpret basic YANG models)*

An interface's IP address appears in the tree like this:

```
+--rw ip
   +--rw (address-choice)?
      +--:(address)
         +--rw address
            +--rw primary
               +--rw address?   inet:ipv4-address
               +--rw mask?      inet:ipv4-address
```

You build an `<edit-config>` to set the primary address. Which is **true**?

- **A.** The XML must include an `<address-choice>` element wrapping
  `<primary>`.
- **B.** `(address-choice)` and `:(address)` are schema-only constructs — they
  don't appear as elements in the XML; you go straight from `<address>` to
  `<primary>`.
- **C.** `(address-choice)` is a container you must send empty to select it.
- **D.** The `?` means the whole `ip` branch is read-only.

<details>
<summary>Answer</summary>

**Correct answer: B**

A YANG **`choice`** (shown as `( )`) and its **`case`** children (`:( )`) are
**schema-only** — they constrain *which* nodes are valid together, but they are
**not data nodes** and never serialize onto the wire. So the payload skips them:

```xml
<ip>
  <address>
    <primary>
      <address>10.0.0.100</address>
      <mask>255.255.255.255</mask>
    </primary>
  </address>
</ip>
```

- **A** and **C** invent elements that don't exist — there's no
  `<address-choice>` tag.
- **D** is wrong — `+--rw` means **read-write** (config); the `?` marks the
  choice as **optional**, not read-only (read-only would be `+--ro`).

</details>

---

## Question 6 — Choosing the NETCONF operation

*(Exam topic 3.8 / 5.10 — operations and read vs. write)*

Using YANGSuite you first read the current loopbacks, then create a new one,
then read again to confirm. Which sequence of NETCONF operations matches that
"read → create → confirm" flow?

- **A.** `<get-config>` → `<edit-config>` → `<get-config>`
- **B.** `<edit-config>` → `<get-config>` → `<edit-config>`
- **C.** `<lock>` → `<unlock>` → `<lock>`
- **D.** `<get-config>` → `<get-config>` → `<get-config>`

<details>
<summary>Answer</summary>

**Correct answer: A**

- **Read** the loopbacks → `<get-config>` (returns `<data>`).
- **Create** the new loopback → `<edit-config>` (returns `<ok/>`).
- **Confirm** it exists → `<get-config>` again.

This is the NETCONF twin of Episode 4's RESTCONF `GET → PUT → GET` loop.

- **B** uses a write to read — wrong.
- **C** only locks/unlocks; it never reads or writes config.
- **D** never writes, so nothing is ever created.

</details>

---

## Question 7 — NETCONF port and simulation tooling

*(Exam topics 6.7 and 5.3)*

You spin up a **Catalyst 8000v in Cisco Modeling Labs** and enable
`netconf-yang`, but YANGSuite can't connect. A colleague asks two things. Which
pair is correct?

- **A.** NETCONF listens on **TCP 830**, and **Cisco Modeling Labs (CML)** is a
  network simulation/virtualization tool — a valid place to run the lab device.
- **B.** NETCONF listens on **TCP 443**, and CML is a configuration-management
  tool like Ansible.
- **C.** NETCONF listens on **UDP 161**, and CML is a packet analyzer.
- **D.** NETCONF listens on **TCP 22**, and CML is a cloud API gateway.

<details>
<summary>Answer</summary>

**Correct answer: A**

- **NETCONF = TCP 830** (topic 6.7). If YANGSuite can't reach the device, that
  port between your host and the Catalyst 8000v is the first thing to check. (Port 22
  is ordinary SSH; 443 is HTTPS/RESTCONF; 161 is SNMP.)
- **Cisco Modeling Labs** is a **network simulation/modeling** tool (topic 5.3,
  alongside pyATS) — exactly what's hosting the Catalyst 8000v in this episode.

- **B**, **C**, **D** each get the port wrong and mischaracterize CML.

</details>

---

## Question 8 — YANG model flavors (multiple answer — pick 3)

*(Exam topic 5.11 / 3.8 — recognize the model flavors)*

The episode uses the **native** model but reminds you it's one of several
flavors. Which **three** of the following are legitimate categories ("flavors")
of YANG data models? **(Choose three.)**

- **A.** OpenConfig — a vendor-neutral, industry-consortium model
- **B.** IETF — models published by the standards body (e.g. `ietf-interfaces`)
- **C.** Native — the vendor's own device-specific model (e.g.
  `Cisco-IOS-XE-native`)
- **D.** NETCONF — a YANG flavor tied to TCP port 830
- **E.** RESTCONF — a YANG flavor that only exists over HTTPS
- **F.** SNMP-MIB — a YANG flavor defined by SNMP MIBs

<details>
<summary>Answer</summary>

**Correct answers: A, B, C**

The three commonly cited YANG **model flavors**:

- **A — OpenConfig:** vendor-neutral models from the OpenConfig consortium.
- **B — IETF:** models standardized by the IETF (RFC-defined).
- **C — Native:** the vendor's own model (e.g. `Cisco-IOS-XE-native`) — most
  complete for that platform, least portable.

Why the others are wrong:

- **D — NETCONF** and **E — RESTCONF** are **transports/protocols** that
  *carry* YANG data — not model flavors. (Note they're independent of flavor:
  you can carry any flavor over either.)
- **F — SNMP-MIB** is a different management framework (SMI/MIBs), not a YANG
  flavor.

</details>

---

### Exam-topic coverage summary

| Question | Focus | Correct | Topic(s) |
|----------|-------|---------|----------|
| 1 | What NETCONF is (vs. RESTCONF / screen-scraping) | B | 3.8 |
| 2 | NETCONF vs. RESTCONF (transport, port, encoding) | A | 3.8, 6.7 |
| 3 | Interpreting a returned `<rpc-reply>` payload | B | 5.10 |
| 4 | Reading a YANG tree (container/list/leaf/namespace) | B | 5.11 |
| 5 | `choice`/`case` are schema-only, not on the wire | B | 5.11 |
| 6 | Read vs. create vs. confirm (get-config/edit-config) | A | 3.8, 5.10 |
| 7 | NETCONF port (830) + CML's role | A | 6.7, 5.3 |
| 8 | YANG model flavors — native / OpenConfig / IETF (pick 3) | A, B, C | 5.11, 3.8 |
