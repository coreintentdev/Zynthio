#!/usr/bin/env python3
"""Ingest new Cloudflare domains into corpus"""
import json, urllib.request, time, subprocess, os

token = 'cfut_UXf3xXZOSB7CZzddF6ELUSSvilVLYaP4efljSbxm602569de'

# Get all zones
all_zones = []
page = 1
while True:
    req = urllib.request.Request(f'https://api.cloudflare.com/client/v4/zones?per_page=100&page={page}&status=active', 
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})
    data = json.load(urllib.request.urlopen(req))
    zones = data['result']
    all_zones.extend(zones)
    if len(zones) < 100:
        break
    page += 1

# Filter new domains (last 7 days)
import datetime
week_ago = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).isoformat()
new_domains = [z['name'] for z in all_zones if z['created_on'] > week_ago]

print(f'Found {len(new_domains)} new domains to ingest')
print('Sample domains:', new_domains[:10])

# Save new domains list
with open('/root/zynthio/corpus/new_cloudflare_domains_20260821.txt', 'w') as f:
    for domain in new_domains:
        f.write(domain + '\n')

print(f'\nSaved new domains list to /root/zynthio/corpus/new_cloudflare_domains_20260821.txt')
print('Ready for corpus ingestion')
