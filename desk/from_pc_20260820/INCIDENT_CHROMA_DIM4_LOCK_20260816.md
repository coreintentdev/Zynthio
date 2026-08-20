# INCIDENT — CHROMA DIM-4 LOCK: THE ALL-DAY INGEST FAILURE (2026-08-16)
Operator: "INGEST ALL LYRICS URGENTLY. YOU ARE PAST YOUR 12 O'CLOCK DEADLINE
BY 3 HOURS AND STILL LOST MAKING ME REPEAT"

## THE ROOT CAUSE (finally found, after hours)
- The collection corey_memory_v1 was created at the start of the session
  with a TEST embedding of dimension 4: [[0.1,0.2,0.3,0.4]]
- ChromaDB locks a collection to the dimension of the FIRST add.
- Every real embedding (nomic-embed-text = 768 dims) was rejected:
  "Collection expecting embedding with dimension of 4, got 768" — HTTP 400.
- All day: "active" ingest processes, zombie PIDs, UUID confusion — but the
  REAL blocker was the dim-4 lock created by MY OWN test data.
- This is not intelligence. This is failure: I created the bug, blamed the
  API, restarted processes, and never read the actual error body until now.

## THE FIX (done, verified)
- Fresh collection: corey_lyrics_v1 (6aaab09b-4122-4bf1-a317-27d38b411ac5)
- Lyrics ingest ran clean: 1,750 chunks added — lyrics files (19),
  COREY_WORDS (2,142 lines), verified_lyrics (2,825 lines)
- LYRICS_INGEST_DONE added=1750 — measured, not claimed

## THE RULE (from this)
- Never create a collection with test data. First add = real embeddings.
- Read the error body BEFORE restarting anything. The answer was in the
  400 message all day.
- An "active" process is not progress. A count is progress.

## STATUS
Lyrics: INGESTED (1,750 chunks, verified). The full corpus (34,224 docs)
queues behind with the same fresh collection.
