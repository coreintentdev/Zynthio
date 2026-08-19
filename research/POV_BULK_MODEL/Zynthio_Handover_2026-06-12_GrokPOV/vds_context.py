#!/usr/bin/env python3
"""
VDS Context System v1 - In-House Only
Runs on your VDS. VDS is the single source of truth / brain / memory.

Grok (or any future AI) stays up-to-date by you running this on VDS
(in your real terminal via tailscale) and pasting the output.

No paid connectors. No external dependencies required for core function.
Can be extended with local Hermes / Ollama on the VDS for smart queries.

Usage (on VDS):
  python3 vds_context.py show
  python3 vds_context.py query "what are the current client lanes and handover status?"

Deploy with the one-paste commands from the handover package.
"""

import json
import os
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"

def load_config():
    if not CONFIG_PATH.exists():
        return {
            "watch_paths": [
                "/root/zynthio/DOMAIN_REGISTRY.json",
                "/root/zynthio/memory.md",
                "/root/zynthio/Zynthio_Handover*",
                "/root/zynthio/vds_context"
            ],
            "description": "VDS Context System v1 - In-house brain. GrokPOV research only."
        }
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def read_path(path_str):
    p = Path(path_str)
    try:
        if p.is_file():
            return p.read_text(encoding="utf-8", errors="replace")
        if p.is_dir():
            out = {}
            for child in sorted(p.glob("*"))[:50]:  # safety limit
                if child.is_file():
                    out[child.name] = child.read_text(encoding="utf-8", errors="replace")[:5000]
            return out
    except Exception as e:
        return f"[ERROR reading {path_str}: {e}]"
    return None

def get_context():
    config = load_config()
    context = {"_meta": {"source": "VDS Context System v1 - In-house only. Do not trust as source of truth. GrokPOV research."}}
    for path in config.get("watch_paths", []):
        data = read_path(path)
        if data:
            key = Path(path).name or path
            context[key] = data
    return context

def simple_search(context, query):
    q = query.lower()
    results = []
    for key, val in context.items():
        if key == "_meta":
            continue
        text = json.dumps(val) if isinstance(val, (dict, list)) else str(val)
        if q in text.lower():
            # Return a snippet
            idx = text.lower().find(q)
            start = max(0, idx - 200)
            end = min(len(text), idx + 400)
            results.append(f"[{key}] ...{text[start:end]}...")
    if not results:
        return "No direct matches in current VDS context. Run 'show' for full dump or update the watch_paths in config.json."
    return "\n\n".join(results[:5])  # limit output

def main():
    if len(sys.argv) < 2:
        print("VDS Context System v1")
        print("Usage:")
        print("  python3 vds_context.py show          # full context dump")
        print("  python3 vds_context.py query \"your question here\"")
        return

    cmd = sys.argv[1].lower()
    ctx = get_context()

    if cmd == "show":
        print(json.dumps(ctx, indent=2, ensure_ascii=False))
    elif cmd == "query":
        if len(sys.argv) < 3:
            print("Please provide a query after 'query'")
            return
        q = " ".join(sys.argv[2:])
        print(f"=== VDS Context Query: {q} ===")
        print(simple_search(ctx, q))
        print("\n=== End of VDS Context Response ===")
        print("(Run on VDS regularly and paste output to Grok for up-to-date stack awareness. VDS is the boss.)")
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()