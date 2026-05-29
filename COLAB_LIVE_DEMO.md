# Colab Live Demo One-Cell Launcher

Paste this into one Colab code cell and run it before the presentation.

```python
import os
import subprocess
import sys
from pathlib import Path

from google.colab import drive

REPO_URL = "https://github.com/helloiamhojun/k-privacy-filter.git"
WORKDIR = Path("/content/k-privacy-filter")
DRIVE_ROOT = Path("/content/drive/MyDrive/k-privacy-filter")


def run(command, cwd=None):
    print(f"\n$ {' '.join(command)}")
    subprocess.run(command, cwd=cwd, check=True)


print("[1/5] Mounting Google Drive")
drive.mount("/content/drive", force_remount=False)
DRIVE_ROOT.mkdir(parents=True, exist_ok=True)

print("[2/5] Loading latest KPF code")
if WORKDIR.exists() and (WORKDIR / ".git").exists():
    run(["git", "fetch", "origin"], cwd=WORKDIR)
    run(["git", "reset", "--hard", "origin/main"], cwd=WORKDIR)
else:
    if WORKDIR.exists():
        run(["rm", "-rf", str(WORKDIR)])
    run(["git", "clone", REPO_URL, str(WORKDIR)])

print("[3/5] Installing dependencies")
run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"], cwd=WORKDIR)

print("[4/5] Checking OPF import")
run([sys.executable, "-c", "from opf import OPF; print('OPF import OK')"], cwd=WORKDIR)

print("[5/5] Starting live Gradio demo")
print("Look for: Running on public URL: https://xxxxx.gradio.live")
print("Keep this cell running during the live demo.")
os.chdir(WORKDIR)
run([sys.executable, "scripts/demo.py"], cwd=WORKDIR)
```

Notes:

- Use the `https://*.gradio.live` URL for the presentation.
- The first run may download the OPF checkpoint, so start this a few minutes before the demo.
- If Colab reconnects, run the same cell again.
