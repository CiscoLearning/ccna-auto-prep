#let's build a Virtual Env

python3 -m venv .venv            # make an isolated Python just for this project
source .venv/bin/activate        # use it (your prompt shows "(.venv)")
pip install -r requirements.txt  # packages land in .venv, not your system