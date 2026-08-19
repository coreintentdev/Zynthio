#!/bin/zsh
# COR Terminal v2 — Interactive Sovereign Edition
# For both local Mac + VDS
# Theme: 336 | Happy Hardcore | No dumb terminal

# ============================================
# CORE SETUP
# ============================================
export COR_THEME="336"
export ZYNTHIO_ROOT="$HOME/zynthio-tools"
export COR_COLOR="cyan"

# Colors
autoload -U colors && colors
COR_CYAN="%F{cyan}"
COR_GREEN="%F{green}"
COR_YELLOW="%F{yellow}"
COR_RESET="%f"

# ============================================
# PROMPT — Beautiful Interactive Prompt
# ============================================
PROMPT='${COR_CYAN}COR ${COR_GREEN}%1~ ${COR_YELLOW}→ ${COR_RESET}'
RPROMPT='%F{8}[336] %F{cyan}%*'

# ============================================
# KEY BINDINGS & INTERACTIVITY
# ============================================
bindkey '^R' history-incremental-search-backward
bindkey '^[[A' up-line-or-search
bindkey '^[[B' down-line-or-search

# fzf integration (if installed)
if command -v fzf >/dev/null; then
  source <(fzf --zsh 2>/dev/null || true)
fi

# ============================================
# ZYNRIP + SOVEREIGN COMMANDS
# ============================================
alias zynrip="python $ZYNTHIO_ROOT/zynrip/zynrip_github_harvester.py"
alias zynrip-receiver="python $ZYNTHIO_ROOT/zynrip_extension_receiver.py"
alias harvest-suno="python $ZYNTHIO_ROOT/zynrip/zynrip_suno_harvester.py"   # to be created
alias master-seamstress="cat $ZYNTHIO_ROOT/_context/MASTER_SEAMSTRESS_CONTEXT_*.md | tail -50"
alias save-on-the-fly="echo 'save on the fly triggered' && python $ZYNTHIO_ROOT/zynthio_connector_blueprint.py --save"

# Quick access to key tools
alias sites="cat $ZYNTHIO_ROOT/_meta/DOMAIN_REGISTRY.json | jq 'keys[]' 2>/dev/null || ls $ZYNTHIO_ROOT"
alias stack="echo 'VDS + Local + Open Claw + Hermes + ZYNRIP active'"
alias state="echo 'IS_VDS='"${IS_VDS:-false}"' | 336 mode | COR Terminal v2'"

# ============================================
# OPENAI CLI INTEGRATION (you just installed this)
# ============================================
alias oai="openai"
alias imagine="openai api images.create --prompt"
alias chat="openai api chat.completions.create --model gpt-4o --message user:"

# Superpower: Generate logos for sites/agents
logo-for-site() {
  local site=$1
  local prompt="Minimalist cyberpunk logo for $site, black background, cyan and magenta accents, 336 Hz wave motif, clean vector style, professional, sovereign tech aesthetic"
  echo "Generating logo for $site..."
  openai api images.create --prompt "$prompt" --n 1 --size 1024x1024 --output /tmp/${site}_logo.png
  echo "Saved to /tmp/${site}_logo.png (copy to assets folder)"
}

# Batch logo generation for all major brands
generate-all-logos() {
  echo "Generating logos for core ZYNTHIO brands..."
  logo-for-site "Zynthio"
  logo-for-site "wrabbit"
  logo-for-site "pal.lat"
  logo-for-site "SongPal"
  logo-for-site "336"
  logo-for-site "Rappal"
  echo "Core logos generated. Use the prompt library for the remaining 47 domains."
}

# ============================================
# VDS vs LOCAL DETECTION (Interactive)
# ============================================
if [[ "$(hostname)" == vmi* ]] || [[ -d /root/zynthio ]]; then
  export IS_VDS=true
  echo "${COR_CYAN}VDS node detected — full interactive mode enabled${COR_RESET}"
else
  export IS_VDS=false
  echo "${COR_CYAN}Local machine — same powerful interactive experience${COR_RESET}"
fi

# ============================================
# WELCOME + STATUS
# ============================================
echo ""
echo "${COR_CYAN}╔════════════════════════════════════════════════════════════╗"
echo "║  COR Terminal v2 — Interactive Sovereign Mode              ║"
echo "║  336 | Happy Hardcore | No dumb terminal                   ║"
echo "╚════════════════════════════════════════════════════════════╝${COR_RESET}"
echo ""
echo "Type ${COR_YELLOW}corey_sync 336zm${COR_RESET} to engage full pipeline"
echo "Type ${COR_YELLOW}zynrip --help${COR_RESET} or ${COR_YELLOW}generate-all-logos${COR_RESET}"
echo ""

# Make sure this file is sourced in your .zshrc
# Add this line to ~/.zshrc:
# source ~/zynthio-tools/COR_Terminal_Interactive_v2.sh