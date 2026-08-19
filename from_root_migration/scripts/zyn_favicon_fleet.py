#!/usr/bin/env python3
"""ZYN favicon fleet — generate per-domain SVG + inject <link> tags into static HTML."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

FAVICON_LINKS = """  <link rel="icon" href="/favicon.svg" type="image/svg+xml">

  <link rel="apple-touch-icon" href="/apple-touch-icon.svg">"""

THEMES: dict[str, dict[str, str]] = {
    "brisasmarinas.rest": {"letter": "B", "bg": "#08131c", "fg": "#63d1ff", "accent": "#13b2a9"},
    "dog.band": {"letter": "🐕", "bg": "#0d0d0d", "fg": "#f5a623", "accent": "#f5a623"},
    "cisum.dog": {"letter": "↩", "bg": "#000000", "fg": "#00ff00", "accent": "#00ff00"},
    "esrever.fyi": {"letter": "⇄", "bg": "#1a0033", "fg": "#c084fc", "accent": "#a855f7"},
    "nslookup.co": {"letter": "N", "bg": "#0b1220", "fg": "#38bdf8", "accent": "#0ea5e9"},
    "reversepep.com": {"letter": "P", "bg": "#111827", "fg": "#f472b6", "accent": "#ec4899"},
    "336orchestra.xyz": {"letter": "336", "bg": "#12081f", "fg": "#fbbf24", "accent": "#f59e0b"},
    "336.life": {"letter": "336", "bg": "#12081f", "fg": "#fbbf24", "accent": "#f59e0b"},
    "songpal.studio": {"letter": "S", "bg": "#1a0a2e", "fg": "#e879f9", "accent": "#d946ef"},
    "zynthio.ai": {"letter": "Z", "bg": "#050816", "fg": "#22d3ee", "accent": "#06b6d4"},
    "askwhy.dev": {"letter": "?", "bg": "#0f172a", "fg": "#a3e635", "accent": "#84cc16"},
    "songible.com": {"letter": "♪", "bg": "#1e1b4b", "fg": "#fcd34d", "accent": "#f59e0b"},
}

ICON_RE = re.compile(
    r'<link[^>]+rel=["\'](?:shortcut )?icon[^>]*>\s*',
    re.I,
)
APPLE_RE = re.compile(
    r'<link[^>]+rel=["\']apple-touch-icon[^>]*>\s*',
    re.I,
)
HAS_FAVICON = re.compile(r'rel=["\'](?:shortcut )?icon', re.I)


def domain_from_path(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    parts = rel.parts
    if len(parts) >= 2 and parts[0] == "output":
        return parts[1]
    if path.parent.name in ("html", "stack", "apply", "roster", "privacy"):
        return path.parent.parent.name
    if path.parent.name.endswith((".rest", ".band", ".dog", ".fyi", ".com", ".dev", ".wiki", ".xyz", ".live", ".studio", ".app", ".codes", ".de", ".org", ".pics", ".toys", ".news", ".directory", ".deals", ".ai", ".co")):
        return path.parent.name
    return path.parent.name


def theme_for(domain: str) -> dict[str, str]:
    base = domain.lower().removeprefix("www.")
    if base in THEMES:
        return THEMES[base]
    for key, val in THEMES.items():
        if base.endswith(key) or key in base:
            return val
    if base.startswith("336") or "336" in base:
        return {"letter": "336", "bg": "#12081f", "fg": "#fbbf24", "accent": "#f59e0b"}
    h = hashlib.sha256(base.encode()).hexdigest()
    bg = f"#{h[0:6]}"
    fg = f"#{h[6:12]}"
    letter = (base.split(".")[0][:1] or "Z").upper()
    return {"letter": letter, "bg": bg, "fg": fg, "accent": fg}


def svg_for(theme: dict[str, str]) -> str:
    letter = theme["letter"]
    bg, fg, accent = theme["bg"], theme["fg"], theme["accent"]
    size = "11" if len(letter) > 1 else "18"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" role="img" aria-label="site icon">
  <rect width="32" height="32" rx="7" fill="{bg}"/>
  <circle cx="26" cy="6" r="3" fill="{accent}" opacity="0.9"/>
  <text x="16" y="22" text-anchor="middle" font-family="system-ui,-apple-system,sans-serif" font-size="{size}" font-weight="700" fill="{fg}">{letter}</text>
</svg>
"""


def inject_links(html: str) -> str:
    if HAS_FAVICON.search(html):
        html = ICON_RE.sub("", html)
        html = APPLE_RE.sub("", html)
    insert_at = re.search(r"<head[^>]*>", html, re.I)
    if not insert_at:
        return html
    pos = insert_at.end()
    return html[:pos] + "\n" + FAVICON_LINKS + html[pos:]


def process_site_dir(site_dir: Path, domain: str, dry_run: bool = False) -> bool:
    index = site_dir / "index.html"
    if not index.is_file():
        return False
    theme = theme_for(domain)
    svg = svg_for(theme)
    html = index.read_text(encoding="utf-8", errors="replace")
    new_html = inject_links(html)
    changed = new_html != html or not (site_dir / "favicon.svg").exists()
    if dry_run:
        print(f"  [dry] {domain} -> {site_dir}")
        return changed
    (site_dir / "favicon.svg").write_text(svg, encoding="utf-8")
    (site_dir / "apple-touch-icon.svg").write_text(svg, encoding="utf-8")
    index.write_text(new_html, encoding="utf-8")
    print(f"  OK {domain}")
    return True


def process_html_file(html_path: Path, root: Path, dry_run: bool = False) -> bool:
    domain = domain_from_path(html_path, root)
    return process_site_dir(html_path.parent, domain, dry_run=dry_run)


def scan_root(root: Path, dry_run: bool = False) -> tuple[int, int]:
    count = 0
    seen: set[Path] = set()
    for html in sorted(root.rglob("index.html")):
        if any(p in html.parts for p in (".git", "node_modules", "ttl", "_TO_DELETE", "tutabackup")):
            continue
        site_dir = html.parent
        if site_dir in seen:
            continue
        seen.add(site_dir)
        domain = domain_from_path(html, root)
        if process_site_dir(site_dir, domain, dry_run=dry_run):
            count += 1
    return count, len(seen)


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    targets = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not targets:
        targets = [str(Path(__file__).resolve().parent)]
    total = 0
    for t in targets:
        root = Path(t).resolve()
        if not root.exists():
            print(f"SKIP missing {root}")
            continue
        print(f"=== {root} ===")
        if root.is_file() and root.name == "index.html":
            if process_html_file(root, root.parent.parent, dry_run=dry_run):
                total += 1
        else:
            n, _ = scan_root(root, dry_run=dry_run)
            total += n
    print(f"DONE: {total} site dirs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())