import json

# Load the detailed domain data
with open('/root/all_new_domains_detailed_20260821.json', 'r') as f:
    new_domains = json.load(f)

# Extract domain names
domain_names = [d['name'] for d in new_domains]

# Update the new domains file
with open('/root/zynthio/corpus/new_cloudflare_domains_20260821.txt', 'w') as f:
    for domain in domain_names:
        f.write(domain + '\n')

# Read existing cloudflare_domains.txt
try:
    with open('/root/zynthio/corpus/cloudflare_domains.txt', 'r') as f:
        existing_domains = set(line.strip() for line in f if line.strip())
except:
    existing_domains = set()

# Add new domains (avoiding duplicates)
all_domains = existing_domains.union(set(domain_names))

# Write updated master list
with open('/root/zynthio/corpus/cloudflare_domains.txt', 'w') as f:
    for domain in sorted(all_domains):
        f.write(domain + '\n')

print(f'Updated domain lists:')
print(f'  New domains: {len(domain_names)}')
print(f'  Previous total: {len(existing_domains)}')
print(f'  New total: {len(all_domains)}')
print(f'  Domains added: {len(domain_names) - len(existing_domains.intersection(domain_names))}')
