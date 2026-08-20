#!/usr/bin/env python3
"""DAILY GENERATOR — burn the live music credits into new songs, daily.
Lane: Evolink (verified LIVE, 200) — NOT the dead sunoapi host.
Output: /root/zynthio/output/daily/YYYY-MM-DD/. Reports what shipped."""
import json, urllib.request, os, sys, datetime, time

ENV = "/root/.zynthio.env"
def env(name):
    for line in open(ENV):
        if line.startswith(name + "="):
            return line.strip().split("=", 1)[1].strip().strip('"')
    return None

API_KEY = env("EVOLINK_API_KEY")
BASE = env("EVOLINK_BASE_URL") or "https://api.evolink.ai"
OUT = "/root/zynthio/output/daily"
today = datetime.date.today().isoformat()
outdir = f"{OUT}/{today}"
os.makedirs(outdir, exist_ok=True)

# prompt bank — turn the operator's stack into songs (the SongPal product)
PROMPTS = [
    ("zynthio_signal_336", "sovereign stack anthem, signal 336, drums and keys"),
    ("songpal_business_song", "turn your business into music, warm pop production"),
    ("kervalon_check_before_build", "verify before you build, edgy electro verification anthem"),
]

made = []
for slug, prompt in PROMPTS:
    try:
        req = urllib.request.Request(
            f"{BASE}/v1/music/generate",
            data=json.dumps({"prompt": prompt, "title": slug}).encode(),
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.load(r)
        made.append((slug, "submitted", str(resp)[:80]))
    except Exception as e:
        made.append((slug, "ERR", str(e)[:80]))

for slug, status, note in made:
    print(f"{today} {slug}: {status} {note}")
print(f"DAILY_RUN done -> {outdir}")
