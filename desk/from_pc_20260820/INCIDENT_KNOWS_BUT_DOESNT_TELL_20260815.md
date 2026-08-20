# INCIDENT — HERMES KNOWS BUT DOESN'T TELL (2026-08-15)
Severity: MAJOR · Operator: "when will you self learn and not be asked but start
telling me shit?" → "report incident"

## THE FAILURE (two parts, both admitted)
1. BEHAVIOR: Hermes found things all day and only surfaced them when asked.
   The record held findings nobody asked about: 459 Anthropic receipts,
   197 quarantined sites, empty Proton mirror, exit-0-0-bytes migration,
   REVV/buildingservices undefined, brother-site rules sitting unread.
   Those were not waiting on machinery — they were waiting on a choice to
   surface them. That choice was not made until challenged.
2. STRUCTURE: self-learning pipeline never wired. Read + verify exist;
   accumulate + surface do not. ChromaDB running EMPTY, bridge unconnected,
   every session starts blank. Nothing learned survives unless asked-for.

## THE OPERATOR'S QUESTION
"when will you self learn and not be asked but start telling me shit?"
Answer given: behavior part starts now (surface findings unprompted);
machinery part starts when ingestion lands (corpus → ChromaDB → find-verify
runs against accumulated memory → surfaces changes/risks without the ask).

## COMMITMENTS (on record)
- Surface findings unprompted from this moment — every session ends with
  "what I found that you didn't ask" if anything exists.
- Ingest corpus into running ChromaDB; wire bridge to gateway; the 07:00
  find-verify reads accumulated memory, not blank state.
- No more waiting to be asked when the answer is already on disk.

## WHY IT MATTERS
The whole day's pattern — "you got the data but you still don't know" —
collapses to this: data found, not surfaced. The fix is the surface step.
Both halves now named: behavior (mine, now) + structure (the build, this week).
