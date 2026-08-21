#!/bin/bash
TOKEN="cfut_f7VWf73WjPQeOjYvoElByJx184fFh9slVt99pkQt4fc7818c"
OUTPUT="/root/zynthio/corpus/cloudflare_account2.txt"
page=1
per_page=50
total_zones=0

echo "Starting Cloudflare export with token: $TOKEN"

while true; do
  echo "Fetching page $page..."
  response=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?page=$page&per_page=$per_page"     -H "Authorization: Bearer $TOKEN"     -H "Content-Type: application/json")
  
  total=$(echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['result_info']['total_count'])" 2>/dev/null)
  echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); [print(zone['name']) for zone in data.get('result', [])]" >> $OUTPUT
  
  total_zones=$(wc -l < $OUTPUT)
  echo "Exported $total_zones domains (total: $total)"
  
  if [ "$page" -ge "$((total / per_page + 1))" ]; then
    break
  fi
  
  page=$((page + 1))
  sleep 1
done

echo "Export complete: $total_zones domains"
