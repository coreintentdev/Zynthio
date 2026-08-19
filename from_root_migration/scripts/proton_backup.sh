#!/bin/bash
set -e
echo "=== STEP 1: Configure Proton Drive remote ==="
rclone config create proton protondrive
echo "=== STEP 2: Verify Proton remote works ==="
rclone lsd proton: || { echo "FAILED — Proton not authenticating. Stop here."; exit 1; }
echo "=== STEP 3: Count files before backup ==="
SOURCE_COUNT=$(find /var/www/suno_library -type f | wc -l)
echo "Source file count: $SOURCE_COUNT"
echo "=== STEP 4: Copy to Proton ==="
rclone copy /var/www/suno_library proton:suno_library_backup --progress --transfers 4
echo "=== STEP 5: Verify count matches ==="
PROTON_COUNT=$(rclone lsf proton:suno_library_backup --recursive --files-only | wc -l)
echo "Proton file count: $PROTON_COUNT"
if [ "$SOURCE_COUNT" -eq "$PROTON_COUNT" ]; then
  echo "✅ VERIFIED — counts match ($SOURCE_COUNT files). Safe to delete source."
  echo "Run manually when ready: rm -rf /var/www/suno_library"
else
  echo "❌ MISMATCH — source=$SOURCE_COUNT proton=$PROTON_COUNT. DO NOT DELETE."
  exit 1
fi
echo "=== Disk after ==="
df -h /
