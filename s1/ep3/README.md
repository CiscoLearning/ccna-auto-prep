# CCNA Automation Prep — Season 1, Episode 3: Version Control with Git

This is **Episode 3 of Season 1** of a CCNA Automation prep series. Episode 1 made
API calls and got JSON back; Episode 2 looked at the data formats that JSON lives
in. Both produced files: scripts, configs, device data. This episode covers what you
do with those files next. You put them under version control with Git and run the
everyday operations the exam expects you to know.

> **Maps to CCNA Automation exam topics 1.7 and 1.8** (`a`–`g`). See the official
> [200-901 CCNAAUTO exam topics (PDF)](https://learningcontent.cisco.com/documents/marketing/exam-topics/200-901-CCNAAUTO_v.1.1.pdf).

Everything here is command-line Git, practiced on a small, realistic project: a
Python script that reads a Meraki-shaped device inventory from a local JSON file and
prints it as a table. It reads a file instead of the live API, so you need no Meraki
account, no API key, and no internet. That keeps the focus on Git.

---

## The big idea: three places a change lives

Every Git operation moves a change between three places. Keep this picture in your
head and the commands make sense:

```
 working directory  --git add-->  staging area  --git commit-->  repository
 (your edits)                     (the next snapshot)            (permanent history)
```

Git is the version-control tool that runs on your machine. GitHub, GitLab, and
Bitbucket are hosting services that store a shared copy of a Git repo online. You can
use Git with no hosting service at all, which is how most of this episode works.

---

## 1.7 — The advantages of version control

Version control records every change to your files over time, so you can review a
change, undo it, and work alongside other people safely. For a network automation
engineer that means:

| Advantage | What it buys you |
|-----------|------------------|
| **History & audit trail** | Every change is a dated, attributed snapshot: who changed what, when, and (from the message) why. |
| **Undo / rollback** | Return any file, or the whole project, to a known-good earlier state. Handy when a config change takes down a link. |
| **Collaboration** | Many people edit the same files without emailing `config_final_v2_REALLY.txt` around. Git merges the work together. |
| **Safe experiments** | Try a risky change on a branch, isolated from the working version, and merge it only once it's proven. |
| **Single source of truth** | One authoritative copy instead of drifting copies on laptops and jump boxes. |

---

## Prerequisites

| Tool | Why | Install (macOS) |
|------|-----|-----------------|
| `git` | The version-control tool this episode is about | Pre-installed on most macOS/Linux; else `brew install git` |
| `python3` | Runs the sample script (only to *see* the table; Git works regardless) | Pre-installed; else [python.org](https://www.python.org/downloads/) |
| `rich` | Renders the device list as a colorful table | `pip install rich` |

Set your identity once per machine. Git stamps every commit with your name and
email, so do this before your first commit:

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```

> GUI clients (VS Code's Source Control panel, GitHub Desktop, and the like) run
> these same commands under the hood. The CLI is what the exam tests, so that's what
> we use.

---

## Files in this directory

| File | Summary |
|------|---------|
| [`project/get_devices.py`](./project/get_devices.py) | The sample content you'll version. Reads `devices.json` and prints a [Rich](https://github.com/textualize/rich) table, a local stand-in for ep1's live Meraki call. |
| [`project/devices.json`](./project/devices.json) | A small Meraki-shaped device inventory. The file you'll edit to demonstrate `diff` and a merge conflict. |
| [`project/.gitignore`](./project/.gitignore) | Tells Git which files to never track (secrets, caches, editor junk). |
| [`COMMANDS.md`](./COMMANDS.md) | Every command below, in order, with no prose. A quick copy/paste reference. |

The `project/` folder is your starting content. Copy it into a throwaway sandbox and
practice there; if you wreck it, delete the folder and start over:

```bash
cp -r project ~/git-sandbox        # copy the sample project somewhere safe
cd ~/git-sandbox
git init                           # turn a plain folder into a Git repo
git status                         # Git sees the files as "untracked", nothing committed yet
```

`git init` creates a hidden `.git/` folder. That folder is the whole repository (all
history), living alongside your files. `git status` is your map: run it constantly to
see what changed and what's staged.

---

## 1.8.a — Clone

`git clone` makes a full local copy of a remote repository, including its entire
history, and wires up a link back to where it came from (named `origin`). It's
usually the first command you run on an existing project:

```bash
git clone https://github.com/CiscoLearning/ccna-auto-prep.git
cd ccna-auto-prep
git log --oneline                  # every past commit: you get the history, not just files
git remote -v                      # "origin" points back at the URL you cloned from
```

A clone is not the same as downloading a zip. A zip gives you the files; a clone
gives you the files plus the full history and the `origin` link.

---

## 1.8.b — Add / remove

`git add` moves a change from the working directory into the staging area, the set of
changes you've picked for the next commit. `git rm` removes a file and stages that
removal. Nothing is permanent until you `commit`:

```bash
git add devices.json               # stage one specific file
git add .                          # or stage everything that changed
git status                         # confirm what's now staged

git rm old_notes.txt               # delete a file and stage the removal
git rm --cached secrets.env        # stop tracking a file but keep it on disk
```

> The `.gitignore` file lists paths Git refuses to track: `.env`, `*.key`, caches.
> Once a secret is committed it stays in history forever, so a file holding ep1's
> `MERAKI_API_KEY` is exactly what `.gitignore` keeps out of your repo.

---

## 1.8.c — Commit

A commit is a permanent, named snapshot of everything staged, plus a message that
says why you made the change:

```bash
git commit -m "Add Meraki device inventory script and data"
git log --oneline                  # your new commit appears at the top
```

Each commit gets a unique ID (a SHA hash like `9f3c1a2…`). Write messages in the
imperative mood (`Add…`, `Fix…`, `Update…`), the convention most projects follow.

---

## 1.8.g — Diff

`git diff` shows exactly which lines changed: removed lines are prefixed `-`, added
lines `+`. Use it to review a change before you stage or commit it. Edit
`get_devices.py` and change the table title from `Meraki Devices` to
`📡 Meraki Devices`, then:

```bash
git diff                           # unstaged changes: working directory vs. staged
git add get_devices.py
git diff --staged                  # staged changes: what you'll commit right now
git commit -m "Add emoji to device table title"
```

---

## 1.8.e — Branch

A branch is an independent line of development. You make one, do your work there, and
`main` stays stable the whole time. Create a branch, change a device's IP, and
commit, all without touching `main`:

```bash
git branch                         # list branches; the "*" marks where you are
git checkout -b fix/core-ip        # create a branch and switch to it in one step
# Edit devices.json: change core-sw-01 "lanIp" from "10.1.10.2" to "10.1.10.99"
git add devices.json
git commit -m "Correct core-sw-01 lanIp to .99"
git checkout main                  # switch back; on main the IP is still 10.1.10.2
```

Delete a branch once it's merged with `git branch -d fix/core-ip`.

---

## 1.8.f — Merge and handling conflicts

`git merge` combines the commits from one branch into the branch you're on (be on
`main` when you merge a feature branch in). Most merges happen automatically. A
conflict happens when two branches changed the same line differently. Git can't guess
which you want, so it stops and asks:

```bash
# On main, edit devices.json: change the SAME line "10.1.10.2" -> "10.1.10.5"
git add devices.json
git commit -m "Correct core-sw-01 lanIp to .5"

git merge fix/core-ip              # both branches touched the same line => CONFLICT
git status                         # devices.json shows as "both modified"
```

Git writes conflict markers into `devices.json`:

```
<<<<<<< HEAD
      "lanIp": "10.1.10.5"          what's on main (your current branch)
=======
      "lanIp": "10.1.10.99"         what's coming in from fix/core-ip
>>>>>>> fix/core-ip
```

Resolve it by editing the file to keep only the line you want and deleting the three
marker lines, then stage and commit to finish the merge:

```bash
git add devices.json               # marks the conflict as resolved
git commit                         # completes the merge (Git pre-fills the message)
# git merge --abort                # escape hatch: bail out and return to pre-merge
```

A conflict isn't an error. It's Git handing you a decision only a human can make.

---

## 1.8.d — Push / pull

So far everything has been local. A remote is a copy of the repo somewhere else.
`push` sends your commits up to the remote; `pull` brings the remote's commits down (a
fetch plus a merge). To practice without an account, make your own bare repo (history
only, no working files, which is what a hosting server holds):

```bash
git init --bare ../remote-repo.git       # a stand-in "server"
git remote add origin ../remote-repo.git # register it as "origin"
git push -u origin main                  # send commits up; -u links main to origin/main
git pull                                 # bring commits down (fetch + merge)
```

The everyday rhythm on a shared project is pull, work, commit, push.

---

## Git operations cheat sheet

| Operation | Command | Exam topic | What it does |
|-----------|---------|------------|--------------|
| Clone | `git clone <url>` | 1.8.a | Copy a remote repo (with history) locally |
| Status | `git status` | — | The map: what changed, what's staged |
| Add | `git add <file>` / `git add .` | 1.8.b | Stage a change for the next commit |
| Remove | `git rm <file>` | 1.8.b | Delete a file and stage the deletion |
| Commit | `git commit -m "msg"` | 1.8.c | Save staged changes as a snapshot |
| Diff | `git diff` / `git diff --staged` | 1.8.g | See exactly which lines changed |
| Branch | `git branch` / `git checkout -b <name>` | 1.8.e | List, or create and switch to, a branch |
| Merge | `git merge <branch>` | 1.8.f | Combine another branch into this one |
| Push | `git push` | 1.8.d | Send your commits to the remote |
| Pull | `git pull` | 1.8.d | Bring the remote's commits down |
| Log | `git log --oneline` | — | Review the commit history |
