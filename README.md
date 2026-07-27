# CCNA Automation Prep

A hands-on video series and code companion for preparing for the **Cisco Certified
Network Associate – Automation** exam topics. Each episode pairs short, runnable
examples with the concepts the exam expects you to know — starting from the
fundamentals and building up.

The material is organized into **seasons** and **episodes**:

- A **season** groups a major theme (e.g. APIs, data formats, automation tooling).
- An **episode** is a single, self-contained lesson with its own `README.md`,
  runnable scripts, and any supporting files.

## Index

### Season 1

| Episode | Title | What it covers |
|---------|-------|----------------|
| [s1/ep1](./s1/ep1) | Intro to APIs | REST fundamentals: GET/POST verbs, parsing JSON with `jq`, and reading HTTP status codes. Includes a no-auth (Deck of Cards) and an authenticated (Meraki Dashboard) script set, plus a Bruno collection. |
| [s1/ep2](./s1/ep2) | Data Formats | JSON, YAML, and XML side by side: the same network-device document in all three formats, how objects/arrays/types map between them, and converting losslessly with `yq`. |
| [s1/ep3](./s1/ep3) | Version Control with Git | Why version control matters and the everyday Git operations run live: clone, add/remove, commit, branch, merge (with conflict resolution), diff, and push/pull. A README runbook + bare command sheet, practiced locally on a small Python + JSON Meraki-inventory project — no account or API key needed. |

*More episodes coming as the series continues.*

## How to use this repo

1. Browse to the episode you want under its season folder (e.g. `s1/ep1/`).
2. Open that episode's `README.md` — it lists prerequisites, setup, and how to
   run each example.
3. Follow along with the corresponding video.

## License

Licensed under the [Apache License 2.0](./LICENSE.md). Copyright 2026 Learn with Cisco.
