#!/usr/bin/env python3
import json
import re
from datetime import datetime

# Load current queue
with open('/root/zynthio/BUILD_STACK_QUEUE_LIVE.json', 'r') as f:
    queue = json.load(f)

# Load creative ledger
with open('/root/zynthio-tools/zynthio/COREY_CREATIVE_LEDGER.md', 'r') as f:
    ledger = f.read()

# Extract creative tasks from ledger
creative_tasks = []

# Extract songs
song_pattern = r'##\s*(\d+)\s+([^\n]+)'
songs = re.findall(song_pattern, ledger)
for num, title in songs:
    creative_tasks.append({
        'task': f'Process song: {title}',
        'priority': 0,  # P0 override
        'cluster': 'creative',
        'description': f'Generate audio for song #{num}: {title}',
        'source': 'COREY_CREATIVE_LEDGER.md',
        'added_at': datetime.utcnow().isoformat() + 'Z'
    })

# Extract domain concepts
domain_pattern = r'\*\*(.*?)\*\*\s*—\s*([^\n]+)'
domains = re.findall(domain_pattern, ledger)
for domain, desc in domains:
    if domain.endswith('.com') or domain.endswith('.dev') or domain.endswith('.net'):
        creative_tasks.append({
            'task': f'Secure domain: {domain}',
            'priority': 0,
            'cluster': 'creative',
            'description': desc,
            'source': 'COREY_CREATIVE_LEDGER.md',
            'added_at': datetime.utcnow().isoformat() + 'Z'
        })

# Extract digital twin work
if 'digital twin' in ledger.lower():
    creative_tasks.append({
        'task': 'Continue digital twin development (336 signal)',
        'priority': 0,
        'cluster': 'creative',
        'description': 'Advance coreyai digital twin model with persistent context',
        'source': 'COREY_CREATIVE_LEDGER.md',
        'added_at': datetime.utcnow().isoformat() + 'Z'
    })

# Prepend creative tasks to build_order
queue['build_order'] = creative_tasks + queue['build_order']

# Update hermes_suggested_tasks with creative priority
if 'hermes_suggested_tasks' not in queue:
    queue['hermes_suggested_tasks'] = []

for task in creative_tasks:
    queue['hermes_suggested_tasks'].insert(0, {
        'task': task['task'],
        'priority': 0,
        'cluster': task['cluster'],
        'from': 'CREATIVE_PRIORITY_OVERRIDE',
        'added': task['added_at']
    })

# Write back
with open('/root/zynthio/BUILD_STACK_QUEUE_LIVE.json', 'w') as f:
    json.dump(queue, f, indent=2)

print(f'Added {len(creative_tasks)} creative tasks as P0 priority')
print('Creative tasks now at top of build_order')
