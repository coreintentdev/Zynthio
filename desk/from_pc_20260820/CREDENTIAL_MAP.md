# CREDENTIAL MAP — THE WORD LIVES HERE (2026-08-18)
READ THIS FIRST, EVERY SESSION. Values are in the ENCRYPTED vault.
Never re-hunt the corpus: THE WORD HAS A HOME.

## THE MASTER VAULT (encrypted, canonical)
- File: secure/vault.env.gpg (gpg AES-encrypted copy of /root/.zynthio.env)
- Decrypt: `gpg --batch --yes --decrypt secure/vault.env.gpg`
- Key: Zynthio Vault (844FAB37AD8BC9A2)
- Backed up to Proton (add to next sync)

## WHERE EVERY CREDENTIAL CLASS LIVES (value is always in the vault)
| Class | Canonical source | Path |
|-------|-----------------|------|
| Live env (122 vars) | /root/.zynthio.env | the working env |
| Vault (encrypted full copy) | secure/vault.env.gpg | THIS FILE |
| Environment backups | /root/STACK_LIVE.env + 3 .bak | dated copies |
| May backup | zynthio-tools/STATE_BACKUP_336ZM_20260529/zynthio.env | May 30 |
| Onboarding | zynthio-tools/proton-onboarding/{herms,zynthio}.env | Jun |
| Twilio | zynthio-tools/zynthio/evny/twilio.env | the evny dir |
| Mac STACK_LIVE (zyn CLI key file) | ~/Desktop/zynthio-tools/18JUNE/evny/STACK_LIVE.env | Mac side |
| Groq keys (7 valid) | see CORRECTION_GROK_KEYS_7_VALID_20260818.md | desk |
| Cloudzy panel/DELTA | see INCIDENT_CRED_LOSS_45DAY + panel.cloudzy.com | account hunt |

## HOW TO USE (the rule)
1. Check CREDENTIAL_MAP.md -> know where the class lives
2. Decrypt secure/vault.env.gpg for the value
3. Update the vault when a credential changes (gpg re-encrypt /root/.zynthio.env)
4. NEVER re-hunt the corpus for a value that's in the vault

## THE .env DOCTRINE
- Values in /root/.zynthio.env (live, readable by the stack)
- Encrypted mirror in secure/vault.env.gpg
- Plaintext env files never `git add`ed (only the map + vault .gpg)
- Mac STACK_LIVE.env mirrors to the vault on sync
