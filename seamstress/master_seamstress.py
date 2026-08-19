#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║        MASTER SEAMSTRESS v1.0 — AI Thread Consolidator              ║
║        "One who uses threads to build"                               ║
║        Weaves all AI session threads into a single master context    ║
║        Platforms: Windows | macOS | Linux                            ║
╚══════════════════════════════════════════════════════════════════════╝
 
Sources ripped:
  ◈ Claude Desktop  — ~/.claude/projects/ chat_*.jsonl (base64 decoded)
  ◈ Claude.ai       — exported conversations.json zip
  ◈ ChatGPT / GPT-4 — OpenAI export zip (conversations.json)
  ◈ Grok (xAI)      — export zip or browser localStorage dump
  ◈ Perplexity      — Comet local data + export JSON
  ◈ Brave History   — SQLite (History DB)
  ◈ Chrome History  — SQLite (History DB)
  ◈ Google Drive    — pasted/synced JSON exports
  ◈ Notion          — exported markdown
  ◈ Cursor          — .cursorrules + handover files
 
Output:
  ~/zynrip_seamstress/MASTER_THREADS.md      — full indexed thread list
  ~/zynrip_seamstress/MASTER_CONTEXT.md      — deduplicated key intel
  ~/zynrip_seamstress/THREAD_MAP.json        — machine-readable index
  ~/zynrip_seamstress/HANDOVER_[DATE].md     — Cursor-ready handover
"""

import os
import sys
import json
import base64
import sqlite3
import zipfile
import hashlib
import argparse
import shutil
import platform
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Generator

def ensure_rich():
    try:
        from rich.console import Console
        return True
    except ImportError:
        subprocess_run = __import__("subprocess").run
        subprocess_run([sys.executable, "-m", "pip", "install", "rich", "--quiet"], check=False)
        try:
            from rich.console import Console
            return True
        except ImportError:
            return False

HAS_RICH = ensure_rich()
if HAS_RICH:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.rule import Rule
    from rich import box
    console = Console()
else:
    class _C:
        def print(self, *a, **kw): print(*[str(x) for x in a])
        def rule(self, *a, **kw): print("─"*70)
    console = _C()

VERSION   = "v1.0-seamstress-2026-06-04"
OPERATOR  = "Corey McIVOR"
ENTITY    = "ZYNTHIO LIMITED"

SYSTEM     = platform.system()
IS_WINDOWS = SYSTEM == "Windows"
IS_MAC     = SYSTEM == "Darwin"
HOME       = Path.home()

SEAMSTRESS_DIR = HOME / "zynrip_seamstress"
LOG_FILE       = SEAMSTRESS_DIR / "seamstress.log"

def get_source_paths() -> dict:
    p = {
        "claude_desktop": {
            "label": "Claude Desktop",
            "paths": [
                HOME / ".claude" / "projects",
                HOME / "Library" / "Application Support" / "Claude" / "claude-code-sessions",
                HOME / "Library" / "Application Support" / "Claude" / "local-agent-mode-sessions",
            ],
            "patterns": ["chat_*.jsonl", "*.jsonl"],
        },
        "claude_export": {
            "label": "Claude.ai Export",
            "paths": [HOME / "Downloads", HOME / "Desktop", HOME / "zynthio_exports"],
            "patterns": ["claude_*.zip", "claude-export*.zip", "conversations*.zip", "*.json"],
        },
        "chatgpt": {
            "label": "ChatGPT / GPT-4",
            "paths": [HOME / "Downloads", HOME / "Desktop", HOME / "Documents", HOME / "zynthio_exports"],
            "patterns": ["conversations*.json", "chatgpt*.zip", "openai-export*.zip"],
        },
        "grok": {
            "label": "Grok (xAI)",
            "paths": [HOME / "Downloads", HOME / "Desktop", HOME / "zynthio_exports"],
            "patterns": ["grok*.json", "grok*.zip", "xai-export*.zip", "prod-grok-backend.json"],
        },
        "perplexity": {
            "label": "Perplexity / Comet",
            "paths": [HOME / "Downloads", HOME / "Library" / "Application Support" / "Perplexity", HOME / "zynthio_exports"],
            "patterns": ["perplexity*.json", "comet*.json", "*.perplexity"],
        },
        "cursor": {
            "label": "Cursor / .cursorrules",
            "paths": [HOME / "Desktop", HOME / "Documents", HOME / "zynthio", HOME],
            "patterns": ["CURSOR_HANDOVER*.md", ".cursorrules", "MASTER_HANDOVER.md"],
        },
        "zynrip": {
            "label": "ZYNRIP Prior Harvests",
            "paths": [HOME / "zynrip_temp", HOME / "Desktop" / "zynthio-tools", HOME / "zynthio-tools"],
            "patterns": ["*.md", "ZYNRIP_*.md", "ALPHA*.md", "*.json"],
        },
        "web_status_snapshots": {
            "label": "Web Status Snapshots (will.html, zyn_nav.js, 48-node landings, same websites)",
            "paths": [
                HOME / "Desktop" / "zynthio-tools",
                HOME / "Desktop" / "zynthio-tools" / "31may",
                HOME / "Desktop" / "zynthio-tools" / "WEB_STAGING",
                HOME / "Desktop" / "zynthio-tools" / "VDS_LIVE_SYNC",
                HOME / "Desktop" / "zynthio-tools" / "BATCH",
                Path.cwd(),
            ],
            "patterns": [
                "**/will.html", "**/code/will.html", "**/31may/will.html",
                "**/WEB_STAGING/code/will.html", "**/VDS_LIVE_SYNC/html/code/will.html",
                "**/zyn_nav.js", "**/*nav*.js",
                "WEB_STAGING/**/*.html", "31may/*.html", "VDS_LIVE_SYNC/**/*.html",
                "**/*status*.html", "**/handovers/*Suno*.md"
            ],
        },
    }
    return p

def log(msg: str):
    SEAMSTRESS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{ts} {msg}\n")

def out(level: str, msg: str):
    log(f"[{level}] {msg}")
    colors = {"OK":"green","WARN":"yellow","ERR":"red","INFO":"cyan","FIND":"blue"}
    c = colors.get(level,"white")
    if HAS_RICH:
        console.print(f"  [{c}][{level}][/{c}] {msg}")
    else:
        print(f"  [{level}] {msg}")

def human_size(n: int) -> str:
    for u in ("B","KB","MB","GB"):
        if n < 1024: return f"{n:.1f}{u}"
        n //= 1024
    return f"{n:.1f}TB"

def parse_claude_jsonl(fpath: Path) -> list:
    messages = []
    try:
        with open(fpath, "r", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    obj = json.loads(line)
                    role = obj.get("role", "?")
                    content = obj.get("content", "")
                    if isinstance(content, list):
                        text_parts = []
                        for block in content:
                            if isinstance(block, dict):
                                if block.get("type") == "text":
                                    text_parts.append(block.get("text",""))
                                elif block.get("type") == "tool_result":
                                    text_parts.append(f"[tool_result: {str(block)[:100]}]")
                        content = " ".join(text_parts)
                    elif isinstance(content, str):
                        try:
                            content = base64.b64decode(content).decode("utf-8", errors="replace")
                        except Exception: pass
                    ts = obj.get("created_at") or obj.get("timestamp","")
                    messages.append({"role": role, "content": str(content)[:2000], "ts": ts, "source_file": str(fpath)})
                except json.JSONDecodeError: pass
    except Exception as e:
        out("WARN", f"Claude JSONL parse error {fpath.name}: {e}")
    return messages

def parse_chatgpt_export(src: Path) -> list:
    threads = []
    try:
        if src.suffix == ".zip":
            with zipfile.ZipFile(src) as z:
                names = z.namelist()
                conv_file = next((n for n in names if "conversations" in n.lower() and n.endswith(".json")), None)
                if not conv_file: return []
                data = json.loads(z.read(conv_file))
        else:
            data = json.loads(src.read_text(errors="replace"))

        if isinstance(data, list):
            for conv in data:
                title = conv.get("title","Untitled")
                created = conv.get("create_time","")
                if isinstance(created, (int, float)):
                    created = datetime.fromtimestamp(created).strftime("%Y-%m-%d")
                msgs = []
                mapping = conv.get("mapping", {})
                for node in mapping.values():
                    m = node.get("message")
                    if m and m.get("content"):
                        content = m["content"]
                        if isinstance(content, dict):
                            parts = content.get("parts", [])
                            text = " ".join(str(p) for p in parts if isinstance(p, str))
                        else: text = str(content)
                        role = m.get("author",{}).get("role","?")
                        msgs.append({"role": role, "content": text[:2000]})
                threads.append({"platform":"ChatGPT","title":title,"date":str(created),"messages":msgs})
    except Exception as e:
        out("WARN", f"ChatGPT parse error: {e}")
    return threads

def parse_claude_export(src: Path) -> list:
    threads = []
    try:
        if src.suffix == ".zip":
            with zipfile.ZipFile(src) as z:
                names = z.namelist()
                conv_files = [n for n in names if n.endswith(".json")]
                for cf in conv_files:
                    try:
                        data = json.loads(z.read(cf))
                        if isinstance(data, dict):
                            title = data.get("name","Untitled")
                            msgs_raw = data.get("chat_messages", data.get("messages", []))
                            msgs = []
                            for m in msgs_raw:
                                role = m.get("sender","?")
                                content = m.get("text","")
                                if isinstance(content, list):
                                    content = " ".join(b.get("text","") for b in content if isinstance(b, dict) and b.get("type")=="text")
                                msgs.append({"role": role, "content": str(content)[:2000]})
                            threads.append({"platform":"Claude.ai","title":title,"date":"","messages":msgs})
                    except Exception: pass
    except Exception as e:
        out("WARN", f"Claude.ai export parse error: {e}")
    return threads

def parse_grok_export(src: Path) -> list:
    threads = []
    try:
        if src.suffix == ".zip":
            with zipfile.ZipFile(src) as z:
                for name in z.namelist():
                    if name.endswith(".json"):
                        try:
                            data = json.loads(z.read(name))
                            threads += _parse_grok_json(data)
                        except Exception: pass
        else:
            data = json.loads(src.read_text(errors="replace"))
            threads += _parse_grok_json(data)
    except Exception as e:
        out("WARN", f"Grok parse error: {e}")
    return threads

def _parse_grok_json(data) -> list:
    threads = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                title = item.get("title", item.get("id","Grok Thread"))
                msgs = []
                for m in item.get("messages", item.get("conversation",[])):
                    role = m.get("role", m.get("sender","?"))
                    content = m.get("content", m.get("text",""))
                    msgs.append({"role":role,"content":str(content)[:2000]})
                threads.append({"platform":"Grok","title":str(title),"date":"","messages":msgs})
    elif isinstance(data, dict):
        # Could be an export wrapper, check for conversation items
        if "conversations" in data:
            for item in data["conversations"]:
                conv = item.get("conversation", {})
                title = conv.get("title", conv.get("id", "Grok Thread"))
                date = conv.get("create_time", "")
                msgs = []
                for r in item.get("responses", []):
                    res = r.get("response", {})
                    role = res.get("sender", "?")
                    content = res.get("message", "")
                    msgs.append({"role": role, "content": str(content)[:2000]})
                threads.append({"platform":"Grok","title":str(title),"date":str(date),"messages":msgs})
        else:
            threads.append({"platform":"Grok","title":data.get("title","Grok Export"),"date":"","messages":[
                {"role":"?","content":str(data)[:2000]}
            ]})
    return threads

def scan_source(source_key: str, source_cfg: dict) -> dict:
    found = []
    for base_path in source_cfg["paths"]:
        if not base_path.exists(): continue
        for pattern in source_cfg["patterns"]:
            if "*" in pattern:
                for match in list(base_path.glob(pattern)) + list(base_path.rglob(pattern)):
                    found.append({"path": match, "type": "file"})
            else:
                fp = base_path / pattern
                if fp.exists():
                    found.append({"path": fp, "type": "file"})
    seen = set()
    deduped = []
    for item in found:
        k = str(item["path"])
        if k not in seen:
            seen.add(k)
            deduped.append(item)
    return {"source": source_key, "label": source_cfg["label"], "items": deduped}

def full_scan(include_sources: Optional[list] = None) -> dict:
    sources = get_source_paths()
    report = {}
    for key, cfg in sources.items():
        if include_sources and key not in include_sources: continue
        result = scan_source(key, cfg)
        count = len(result["items"])
        if count: out("FIND", f"{cfg['label']}: {count} item(s) found")
        report[key] = result
    return report

def weave_threads(scan_report: dict) -> dict:
    all_threads = []
    cursor_docs = []
    raw_docs = []

    for source_key, source_data in scan_report.items():
        label = source_data["label"]
        for item in source_data["items"]:
            fp = item["path"]
            if source_key == "claude_desktop" and fp.suffix == ".jsonl":
                msgs = parse_claude_jsonl(fp)
                if msgs:
                    all_threads.append({
                        "platform": "Claude Desktop", "title": f"{fp.parent.name}/{fp.name}",
                        "date": datetime.fromtimestamp(fp.stat().st_mtime).strftime("%Y-%m-%d"),
                        "messages": msgs, "source": str(fp), "sha256": hashlib.sha256(fp.read_bytes()).hexdigest()[:16],
                    })
            elif source_key == "claude_export":
                threads = parse_claude_export(fp)
                for t in threads: t["source"], t["sha256"] = str(fp), hashlib.sha256(fp.read_bytes()).hexdigest()[:16]
                all_threads.extend(threads)
            elif source_key == "chatgpt":
                threads = parse_chatgpt_export(fp)
                for t in threads: t["source"] = str(fp)
                all_threads.extend(threads)
            elif source_key == "grok":
                threads = parse_grok_export(fp)
                for t in threads: t["source"] = str(fp)
                all_threads.extend(threads)
            elif source_key == "cursor":
                try:
                    cursor_docs.append({
                        "filename": fp.name, "path": str(fp), "content": fp.read_text(errors="replace")[:50000],
                        "modified": datetime.fromtimestamp(fp.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                    })
                except Exception: pass
            elif source_key in ("zynrip","notion","web_status_snapshots") and fp.suffix in (".md",".json",".txt",".html",".htm"):
                try:
                    text = fp.read_text(errors="replace")
                    if len(text) > 50:
                        raw_docs.append({
                            "filename": fp.name, "source": source_key, "content": text[:20000],
                            "modified": datetime.fromtimestamp(fp.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                        })
                except Exception: pass
    return {"threads": all_threads, "cursor_docs": cursor_docs, "raw_docs": raw_docs}

INTEL_PATTERNS = [
    r"(?i)(incident\s*#?\d+)", r"(?i)(CRITICAL|URGENT|BLOCKED|FAILED|ERROR|BUG)",
    r"(?i)(deploy(ed|ing)?|migration|VDS|VPS)", r"(?i)(\$[\d,]+\.?\d*\s*(USD|AUD|NZD)?)",
    r"(?i)(API|token|key|secret)\s+\w+", r"(?i)(domain|dns|cloudflare|CF\s)",
    r"(?i)(336zm|protocol 336|zynrip|bifrost|g4.lens)", r"(?i)(todo|action.?item|next step|follow.?up)",
    r"(?i)(WILL LOCK|Status: SAVED|bongo|9:35 PM|will\.html)", r"(?i)(zyn_nav\.js|same website|Status: SAVED)"
]

def extract_key_intel(threads: list) -> list:
    intel = []
    seen_hashes = set()
    for thread in threads:
        platform = thread.get("platform","?")
        title = thread.get("title","?")
        date = thread.get("date","?")
        for msg in thread.get("messages",[]):
            text = msg.get("content","")
            for sentence in re.split(r"[.!?\n]", text):
                sentence = sentence.strip()
                if len(sentence) < 20: continue
                for pattern in INTEL_PATTERNS:
                    if re.search(pattern, sentence):
                        h = hashlib.md5(sentence.lower().encode()).hexdigest()
                        if h not in seen_hashes:
                            seen_hashes.add(h)
                            intel.append({"platform": platform, "thread": title[:60], "date": date, "intel": sentence[:300]})
                        break
    return intel

def generate_master_context(woven: dict) -> str:
    intel = extract_key_intel(woven["threads"])
    cursor = woven["cursor_docs"]
    lines = [
        f"# MASTER CONTEXT — ZYNTHIO C-STACK",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Seamstress: Master Seamstress {VERSION}",
        f"Operator: {OPERATOR}", "", "---", "",
        f"## KEY INTELLIGENCE ({len(intel)} signals extracted)", "",
        "| Platform | Thread | Date | Signal |", "|----------|--------|------|--------|",
    ]
    for item in sorted(intel, key=lambda x: x.get("date",""), reverse=True)[:200]:
        pl, th, dt = item["platform"][:12], item["thread"][:30].replace("|",""), item["date"][:10]
        sig = item["intel"][:100].replace("|","").replace("\n"," ")
        lines.append(f"| {pl} | {th} | {dt} | {sig} |")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description=f"MASTER SEAMSTRESS {VERSION}")
    parser.add_argument("--weave", action="store_true", help="Full scan + write all outputs")
    parser.add_argument("--export", metavar="PATH", help="Add external export file")
    args = parser.parse_args()

    SEAMSTRESS_DIR.mkdir(parents=True, exist_ok=True)
    
    if args.export:
        out("INFO", f"Scanning specific export path: {args.export}")
        # Inject the export path dynamically into the sources
        sources = get_source_paths()
        for k in sources:
            sources[k]["paths"].append(Path(args.export))
    
    scan_report = full_scan()
    woven = weave_threads(scan_report)
    intel = extract_key_intel(woven["threads"])
    
    out("OK", f"Threads woven: {len(woven['threads'])}")
    out("OK", f"Key signals:   {len(intel)}")

    context_md = generate_master_context(woven)
    p2 = SEAMSTRESS_DIR / "MASTER_CONTEXT.md"
    p2.write_text(context_md)
    out("OK", f"MASTER_CONTEXT.md ({human_size(len(context_md))}) written to {p2}")

if __name__ == "__main__":
    main()
