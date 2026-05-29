# Colab Live Demo One-Cell Launcher

Paste this into one Colab code cell and run it before the presentation.

```python
import os
import re
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


def stream_demo(command, cwd=None):
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    print(f"\n$ {' '.join(command)}")
    process = subprocess.Popen(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    try:
        assert process.stdout is not None
        for line in process.stdout:
            print(line, end="")
            match = re.search(r"https://[a-zA-Z0-9.-]+\.gradio\.live", line)
            if match:
                print("\n" + "=" * 72)
                print("LIVE DEMO URL:", match.group(0))
                print("Open this URL for the presentation.")
                print("Keep this Colab cell running while presenting.")
                print("=" * 72 + "\n")
        process.wait()
        if process.returncode:
            raise subprocess.CalledProcessError(process.returncode, command)
    except KeyboardInterrupt:
        print("\nDemo stopped. Run this cell again to reopen the live URL.")
        process.terminate()
        raise


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
stream_demo([sys.executable, "-u", "scripts/demo.py"], cwd=WORKDIR)
```

Notes:

- Use the `https://*.gradio.live` URL for the presentation.
- The first run may download the OPF checkpoint, so start this a few minutes before the demo.
- If Colab reconnects, run the same cell again.
