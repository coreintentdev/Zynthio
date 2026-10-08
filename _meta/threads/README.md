# Workspace threads → VDS

Destination on the VDS: `/root/zynthio/_meta/threads/`

This folder is the git-pipe staging pack. It is **not** landed on the VDS until mesh SSH returns `ssh_ok`.

```bash
npm test
npm run typecheck
bash ops/vds/push-threads.sh
```

Secrets (Cursor environment dashboard — never paste in chat):

- `ZYNTHIO_DC_SSH_KEY` — PEM from Mac `~/.ssh/zynthio_dc`
- `HEADSCALE_PREAUTH_KEY` — Headscale preauth for user `zynthio` at `https://headscale.kamals.pro`

JEV stays on `https://api.typesafe.ai/v1/systemone` (`jev-latest`, 0.85). Hermes stays mesh-only `:8000`.
