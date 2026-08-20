# INCIDENT — SKY-STAY: CRED (USERNAME GIVEN, PW LOST) + CHASE AS SONG (2026-08-20)
Operator: "sky-stay is a username on proton" — corrected my misread.

## THE FACTS (corrected)
- sky-stay is a PROTON LITE USERNAME, NOT a song.
- The password was "lost too" (operator) — a credential-loss case.
- gpg secret-key 844FAB is present (count=1) but the vault
  decrypt returns 0 lines (needs the key passphrase not available
  non-interactively). So the sky-stay/password CANNOT be recovered
  from the vault as-is.
- I earlier matched "sky stays high" as a lyric in backup JSONs — that
  was a FALSE match; the lyric is unrelated to the sky-stay username.

## THE ACTION
- The sky-stay Proton access cannot be recovered from the current vault
  state (0-line decrypt). The username exists; the password is lost.
- This is the SAME credential-loss family as the earlier incidents —
  the "password lost" recurring. The canonical fix (per the
  credential-vault doctrine) is already the gpg vault; the gap is that
  the vault itself now can't unlock without its passphrase.

## STATUS
- No fabrications about being able to read sky-stay — I cannot.
  The password is genuinely unrecoverable from this vault state.
