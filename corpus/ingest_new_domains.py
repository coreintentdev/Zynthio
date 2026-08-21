#!/usr/bin/env python3
"""Ingest new Cloudflare domains into corpus"""
import json, urllib.request, time, subprocess, os, sys

def ingest_domain(domain):
    """Ingest single domain into corpus"""
    try:
        # Use existing corpus ingestion script
        result = subprocess.run(['python3', 'external_domain_ingestor.py', domain], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f'✅ {domain} - SUCCESS')
            return True
        else:
            print(f'❌ {domain} - FAILED: {result.stderr[:100]}')
            return False
    except Exception as e:
        print(f'⚠️  {domain} - ERROR: {str(e)[:100]}')
        return False

# Load new domains
with open('new_cloudflare_domains_20260821.txt', 'r') as f:
    new_domains = [line.strip() for line in f if line.strip()]

print(f'Starting ingestion of {len(new_domains)} new domains...')
print('This will take approximately 4-6 hours')
print('Starting with first 10 domains as test...')

# Test with first 10 domains
test_domains = new_domains[:10]
success_count = 0
for i, domain in enumerate(test_domains, 1):
    print(f'[{i}/{len(test_domains)}] Processing {domain}...')
    if ingest_domain(domain):
        success_count += 1
    time.sleep(2)  # Rate limiting

print(f'\nTest complete: {success_count}/{len(test_domains)} successful')
if success_count >= 7:  # 70% success rate
    print('Test successful. Ready for full ingestion.')
    print('Run full ingestion with: python3 ingest_new_domains.py --full')
else:
    print('Test success rate below threshold. Review issues before full ingestion.')
