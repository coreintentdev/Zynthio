#!/usr/bin/env python3
"""Master Seamstress — VDS edition. Weaves chat exports already on VDS."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "5june"))

import master_seamstress as ms  # noqa: E402

ms.SEAMSTRESS_DIR = Path("/root/zynthio/_meta/seamstress")
ms.LOG_FILE = ms.SEAMSTRESS_DIR / "seamstress.log"
HOME = Path("/root")


def get_source_paths_vds():
    return {
        "claude_desktop": {
            "label": "Claude Desktop / CLI on VDS",
            "paths": [
                HOME / ".claude" / "projects",
                Path("/root/claude_sessions"),
                Path("/root/zynthio/claude-context"),
                Path("/root/zynthio/claude-context/jsonls"),
            ],
            "patterns": ["chat_*.jsonl", "*.jsonl"],
        },
        "claude_export": {
            "label": "Claude.ai / Anthropic exports on VDS",
            "paths": [
                Path("/root/anthropic_data_exports"),
                Path("/root/anthropic_data_export_20260422"),
                Path("/root/zynthio/consolidated_incoming"),
                Path("/root/zynthio/handovers"),
                Path("/root/zynthio/zynvault/exports"),
                Path("/root/VDS_OFFLOAD_20260426"),
            ],
            "patterns": ["claude_*.zip", "claude-export*.zip", "conversations*.zip", "*.json", "HANDOVER*.md"],
        },
        "chatgpt": {
            "label": "ChatGPT exports on VDS",
            "paths": [
                Path("/root/zynthio/consolidated_incoming"),
                Path("/root/zynthio/handovers"),
                Path("/root/handovers"),
            ],
            "patterns": ["conversations*.json", "chatgpt*.zip", "openai-export*.zip"],
        },
        "grok": {
            "label": "Grok exports on VDS",
            "paths": [
                Path("/root/VDS_OFFLOAD_20260426/ZYNTHIO_ARCHIVE/md_bloat_20260423/x_grok_export_mar29"),
                Path("/root/zynthio/consolidated_incoming"),
                Path("/root/zynthio-tools"),
            ],
            "patterns": ["grok*.json", "grok*.zip", "xai-export*.zip", "prod-grok-backend.json"],
        },
        "cursor": {
            "label": "Cursor handovers on VDS",
            "paths": [
                Path("/root/zynthio-tools"),
                Path("/root/zynthio/claude-context/desktop-handovers"),
                Path("/root/zynthio/handovers"),
            ],
            "patterns": ["CURSOR_HANDOVER*.md", ".cursorrules", "MASTER_HANDOVER.md", "*handover*.md"],
        },
        "zynrip": {
            "label": "ZYNRIP prior harvests on VDS",
            "paths": [
                Path("/root/zynthio-tools"),
                Path("/root/zynthio"),
                Path("/root/zynrip-output"),
            ],
            "patterns": ["*.md", "ZYNRIP_*.md", "ALPHA*.md", "*.json", "MASTER_*.md"],
        },
        "web_deploy": {
            "label": "Web / domain deploy artifacts",
            "paths": [
                Path("/root/zynthio-tools/18JUNE"),
                Path("/root/zynthio-tools/VDS_LIVE_SYNC"),
                Path("/var/www"),
            ],
            "patterns": ["*.html", "pork*.json", "domain*.json", "COR*.html"],
        },
    }


ms.get_source_paths = get_source_paths_vds

if __name__ == "__main__":
    ms.main()