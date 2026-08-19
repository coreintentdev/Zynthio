#!/usr/bin/env python3
"""
Find ALL files (md, json, txt, eml, html, chat exports, handovers)
and sync to VDS. Creates comprehensive master index.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# === CONFIGURATION ===
SEARCH_PATHS = [
    Path.home() / "Desktop",
    Path.home() / "Documents", 
    Path.home() / "Downloads",
    Path("/Volumes/R2") if Path("/Volumes/R2").exists() else None,
    Path.home() / ".zynthio" if (Path.home() / ".zynthio").exists() else None,
]
SEARCH_PATHS = [p for p in SEARCH_PATHS if p and p.exists()]

FILE_EXTENSIONS = [
    ".md", ".txt", ".json", ".eml", ".html", ".htm", ".csv", 
    ".yaml", ".yml", ".xml", ".log", ".pdf", ".docx", ".rtf"
]

KEYWORDS = [
    "chat", "claude", "claude-export", "anthropic", "openai", 
    "export", "handover", "handovers", "session", "backup",
    "skill", "song", "336", "zynthio", "zyn", "sunop", "pickleball",
    "gemini", "grok", "perplexity", "cursor", "copilot",
    "domain", "audit", "manifest", "inventory"
]

SKIP_DIRS = [
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    ".fseventsd", ".Spotlight-V100", ".TemporaryItems",
    "_TO_DELETE", ".Trash", "Trash"
]

VDS_HOST = os.environ.get("VDS_HOST", "root@vmi3205024")
VDS_TARGET = f"/root/zynthio/incoming_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
SSH_KEY = Path(os.environ.get("SSH_KEY", str(Path.home() / ".ssh" / "zynthio_dc")))
OUTPUT_DIR = Path.home() / "Desktop" / "zynthio-tools"
MASTER_FILE = OUTPUT_DIR / f"MASTER_ALL_FILES_{datetime.now().strftime('%Y%m%d')}.md"

class FileFinder:
    def __init__(self):
        self.files = []
        self.by_type = defaultdict(list)
        self.by_keyword = defaultdict(list)
        self.total_size = 0
        
    def search(self):
        print("🔍 Searching ALL files...")
        print(f"   Paths: {[str(p) for p in SEARCH_PATHS]}")
        print(f"   Extensions: {len(FILE_EXTENSIONS)} types")
        print()
        
        for base_path in SEARCH_PATHS:
            print(f"Scanning: {base_path}")
            count = 0
            
            try:
                for root, dirs, files in os.walk(base_path):
                    # Skip unwanted directories
                    dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
                    
                    for file in files:
                        filepath = Path(root) / file
                        
                        # Check if file matches criteria
                        ext_match = filepath.suffix.lower() in [e.lower() for e in FILE_EXTENSIONS]
                        keyword_match = any(kw.lower() in file.lower() for kw in KEYWORDS)
                        
                        if ext_match or keyword_match:
                            try:
                                stat = filepath.stat()
                                file_info = {
                                    'path': str(filepath),
                                    'name': file,
                                    'ext': filepath.suffix.lower(),
                                    'size': stat.st_size,
                                    'modified': datetime.fromtimestamp(stat.st_mtime),
                                    'keyword_match': [kw for kw in KEYWORDS if kw.lower() in file.lower()]
                                }
                                self.files.append(file_info)
                                self.by_type[file_info['ext']].append(file_info)
                                self.total_size += stat.st_size
                                
                                for kw in file_info['keyword_match']:
                                    self.by_keyword[kw].append(file_info)
                                
                                count += 1
                                if count % 1000 == 0:
                                    print(f"  ... found {count} files so far")
                                    
                            except (OSError, PermissionError):
                                continue
                                
            except PermissionError:
                print(f"  ⚠️ Permission denied: {base_path}")
                continue
                
        print(f"\n✅ Total found: {len(self.files)} files ({self.total_size / 1024 / 1024:.1f} MB)")
        
    def create_master_index(self):
        print("\n📋 Creating master index...")
        
        with open(MASTER_FILE, 'w', encoding='utf-8') as f:
            f.write(f"# MASTER FILE INDEX - ALL TYPES\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Files:** {len(self.files)}\n")
            f.write(f"**Total Size:** {self.total_size / 1024 / 1024:.1f} MB\n")
            f.write(f"**VDS Target:** {VDS_TARGET}\n\n")
            f.write("---\n\n")
            
            # Summary by type
            f.write("## Summary by File Type\n\n")
            for ext in sorted(self.by_type.keys(), key=lambda x: len(self.by_type[x]), reverse=True):
                files = self.by_type[ext]
                size_mb = sum(f['size'] for f in files) / 1024 / 1024
                f.write(f"- **{ext or '(no ext)'}**: {len(files)} files ({size_mb:.1f} MB)\n")
            f.write("\n")
            
            # Summary by keyword
            f.write("## Summary by Keyword\n\n")
            for kw in sorted(self.by_keyword.keys(), key=lambda x: len(self.by_keyword[x]), reverse=True)[:20]:
                f.write(f"- **{kw}**: {len(self.by_keyword[kw])} files\n")
            f.write("\n")
            
            # Complete file list
            f.write("## Complete File List\n\n")
            for file_info in sorted(self.files, key=lambda x: x['path']):
                size_str = f"{file_info['size'] / 1024:.1f} KB" if file_info['size'] < 1024*1024 else f"{file_info['size'] / 1024 / 1024:.1f} MB"
                mod_str = file_info['modified'].strftime('%Y-%m-%d %H:%M')
                keywords = ', '.join(file_info['keyword_match'][:3]) if file_info['keyword_match'] else ''
                
                f.write(f"- `{file_info['path']}`\n")
                f.write(f"  - Size: {size_str} | Modified: {mod_str}")
                if keywords:
                    f.write(f" | Tags: {keywords}")
                f.write("\n\n")
                
        print(f"✅ Master index: {MASTER_FILE}")
        
    def sync_to_vds(self):
        print(f"\n🚀 Syncing to VDS: {VDS_HOST}:{VDS_TARGET}")
        
        # Create target directory
        result = subprocess.run(
            ["ssh", "-i", str(SSH_KEY), VDS_HOST, f"mkdir -p {VDS_TARGET}"],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            print(f"❌ SSH failed: {result.stderr}")
            return False
            
        print(f"✅ VDS directory created")
        
        # Sync in batches
        BATCH_SIZE = 50
        total = len(self.files)
        synced = 0
        failed = []
        
        print(f"Syncing {total} files...")
        
        for i, file_info in enumerate(self.files):
            src = file_info['path']
            # Create relative path preserving structure
            rel_path = Path(src).relative_to(Path(src).anchor)
            dst = f"{VDS_TARGET}/{rel_path}"
            
            # Ensure parent directory exists
            parent = str(Path(dst).parent).replace(' ', '\ ')
            subprocess.run(
                ["ssh", "-i", str(SSH_KEY), VDS_HOST, f"mkdir -p '{parent}'"],
                capture_output=True
            )
            
            # Copy file
            result = subprocess.run(
                ["scp", "-i", str(SSH_KEY), "-q", src, f"{VDS_HOST}:{dst}"],
                capture_output=True
            )
            
            if result.returncode == 0:
                synced += 1
            else:
                failed.append(src)
                
            if (i + 1) % BATCH_SIZE == 0:
                print(f"  Progress: {i+1}/{total} ({synced} synced, {len(failed)} failed)")
                
        # Copy master index
        subprocess.run(
            ["scp", "-i", str(SSH_KEY), str(MASTER_FILE), f"{VDS_HOST}:{VDS_TARGET}/"],
            capture_output=True
        )
        
        print(f"\n✅ Sync complete: {synced}/{total} files synced")
        if failed:
            print(f"⚠️ Failed: {len(failed)} files")
            
        return True

def main():
    print("═══════════════════════════════════════════")
    print("  ZYNTHIO ALL FILES FINDER + VDS SYNC")
    print("═══════════════════════════════════════════\n")
    
    finder = FileFinder()
    finder.search()
    finder.create_master_index()
    
    print(f"\n📦 Ready to sync to VDS")
    print(f"   Target: {VDS_HOST}:{VDS_TARGET}")
    input("\nPress Enter to start sync (Ctrl+C to cancel)...")
    
    finder.sync_to_vds()
    
    print("\n═══════════════════════════════════════════")
    print("  COMPLETE")
    print("═══════════════════════════════════════════")
    print(f"Master index: {MASTER_FILE}")
    print(f"VDS location: {VDS_TARGET}")
    print("\nTo verify on VDS:")
    print(f"  ssh -i ~/.ssh/zynthio_dc {VDS_HOST} 'ls -la {VDS_TARGET} | head -20'")

if __name__ == "__main__":
    main()
