# ep3 — Command Sheet

Every command from the README, in order, with no prose — a quick copy/paste
reference. Each `###` block maps to one exam topic.

```bash
# --- One-time setup -------------------------------------------------------
git --version
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
pip install rich            # only if you'll run the script

# Make the sandbox from the sample project, then run it once
cp -r project ~/git-sandbox
cd ~/git-sandbox
git init
git status
python3 get_devices.py      # show the table before touching Git
```

### 1.8.a — clone
```bash
git clone https://github.com/CiscoLearning/ccna-auto-prep.git
cd ccna-auto-prep
git log --oneline
git remote -v
cd ..
```

### 1.8.b — add / remove
```bash
git add devices.json
git add .
git status
# git rm old_notes.txt          # delete + stage the removal
# git rm --cached secrets.env   # stop tracking, keep on disk
```

### 1.8.c — commit
```bash
git commit -m "Add Meraki device inventory script and data"
git log --oneline
```

### 1.8.g — diff
```bash
# edit get_devices.py title: "Meraki Devices" -> "📡 Meraki Devices"
git diff
git add get_devices.py
git diff --staged
git commit -m "Add emoji to device table title"
```

### 1.8.e — branch
```bash
git branch
git checkout -b fix/core-ip
# edit devices.json: core-sw-01 lanIp  "10.1.10.2" -> "10.1.10.99"
git add devices.json
git commit -m "Correct core-sw-01 lanIp to .99"
git checkout main
```

### 1.8.f — merge + conflict (in devices.json)
```bash
# on main, edit the SAME line: core-sw-01 lanIp "10.1.10.2" -> "10.1.10.5"
git add devices.json
git commit -m "Correct core-sw-01 lanIp to .5"

git merge fix/core-ip           # -> CONFLICT in devices.json
git status
# open devices.json, delete <<<<<<< ======= >>>>>>> markers, keep the right line
git add devices.json
git commit                      # completes the merge
# git merge --abort             # escape hatch
```

### 1.8.d — push / pull (local bare repo)
```bash
git init --bare ../remote-repo.git
git remote add origin ../remote-repo.git
git push -u origin main
git pull
```
```
