import re
p = "/root/zynthio/seamstress/master_seamstress.py"
src = open(p).read()

# Find the cursor branch end and insert a zynrip generic handler before the final else
# Locate the "elif source_key == \"cursor\":" block and add zynrip handling right after it.
# Simpler: insert a zynrip branch just before "return {" of weave_threads by finding the
# source_key == "notion" or similar generic line. We insert after the cursor/notion branches.

marker = '            elif source_key == "cursor":'
idx = src.find(marker)
if idx == -1:
    # fallback: find any elif in weave_threads
    raise SystemExit("cursor branch not found")

# find the end of the cursor branch (next elif/else at same indent after idx)
# We'll insert a zynrip branch right after the whole if/elif chain by targeting
# the "for source_key" loop's last branch. Instead, insert BEFORE the loop's closing.
# Robust approach: add a helper branch by replacing the line that begins the
# "elif source_key == \"cursor\"" with the same line plus a preceding zynrip branch.

zynrip_branch = '''            elif source_key == "zynrip":
                for it in source_data["items"]:
                    fp = it["path"]
                    if fp.suffix in (".md", ".txt"):
                        try:
                            txt = fp.read_text(encoding="utf-8", errors="replace")
                        except Exception:
                            continue
                        if len(txt.strip()) < 40:
                            continue
                        all_threads.append({
                            "platform": "ZYNRIP", "title": fp.stem,
                            "date": __import__("datetime").datetime.fromtimestamp(fp.stat().st_mtime).strftime("%Y-%m-%d"),
                            "messages": [{"role": "assistant", "content": txt}],
                            "source": str(fp), "sha256": hashlib.sha256(fp.read_bytes()).hexdigest()[:16],
                        })
'''

src = src.replace(marker, zynrip_branch + marker, 1)
open(p, "w").write(src)
print("PATCHED: added zynrip .md/.txt handler to weave_threads")
