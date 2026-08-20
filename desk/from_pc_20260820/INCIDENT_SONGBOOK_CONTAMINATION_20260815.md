# INCIDENT — SONGBOOK CONTAMINATION + UNVERIFIED GENERATION (2026-08-15)
Severity: HIGH (operator correction — AI-ripped lyrics presented as operator's own)

## OPERATOR CORRECTION (verbatim)
- "those are not my lyrics ai ripping my tracks in suno and making it their own."
- "i know my songs. i made them, i got rusty old song book here i will photo."
- "enamour was a title i picked to inspire with love. i think that is the meaning."

## WHAT HAPPENED
- Master songbook file (/root/zynthio/audio/Corey_McIvor_COMPLETE_Songbook/Corey_McIvor_MASTER_SONGBOOK.txt)
  was treated as operator's verified lyrics and used to generate a Suno track
  ("A REFLECTION OF PERFECTION", v1+v2 generated 2026-08-15).
- Operator states the songbook contents are AI-ripped versions of his tracks — NOT his words.
- The generated tracks are therefore UNVERIFIED ART, not operator art.

## WHAT IS VERIFIED (the only provable source)
- /root/zynthio/songpal_lyrics/ROUND_MY_HEAD_RUBY_WESLEY.txt — header: "Source: Corey McIvor — direct lyrics drop, March 24 2026". THIS is his words.
- Twin corpus (twin_corpus/train.jsonl) — his typed messages in context.
- Photos of the physical "rusty old song book" — operator will provide.

## CORRECTIONS (permanent)
1. NEVER generate from the MASTER_SONGBOOK.txt — it is contaminated (AI-ripped).
2. Only "direct lyrics drop" marked files (ROUND_MY_HEAD pattern) are operator lyrics.
3. New operator title logged: ENAMOUR — "to inspire with love" (operator-picked title).
4. Operator can verify every track against his knowledge ("i can go through all. i know my songs").

## STATUS
- A-REFLECTION-OF-PERFECTION v1/v2: generated, marked UNVERIFIED, not presented as operator art.
- Waiting: operator photos of physical songbook → then rebuild the verified catalog from the photos, not the contaminated file.
