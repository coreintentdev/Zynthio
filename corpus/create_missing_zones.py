#!/usr/bin/env python3
import requests
import json
import time

TOKEN = 'cfut_f7VWf73WjPQeOjYvoElByJx184fFh9slVt99pkQt4fc7818c'
ACCOUNT_ID = 'a61bf8a23a8488f6e4257e7127c70b76'
VDS_IP = '5.189.143.170'
PORKBUN_ONLY = '/root/zynthio/corpus/porkbun_only.txt'
RESULTS = '/root/zynthio/corpus/zone_creation_results.json'

def get_porkbun_only_domains():
    comm_result = requests.get('https://api.cloudflare.com/client/v4/zones?page=1&per_page=50',
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'})
    existing = set([zone['name'] for zone in comm_result.json().get('result', [])])
    
    with open('/root/zynthio/corpus/porkbun_domains.txt', 'r') as f:
        porkbun = set([line.strip() for line in f])
    
    porkbun_only = porkbun - existing
    with open(PORKBUN_ONLY, 'w') as f:
        for domain in sorted(porkbun_only):
            f.write(domain + '\n')
    
    return sorted(porkbun_only)

def create_zone(domain):
    response = requests.post(
        'https://api.cloudflare.com/client/v4/zones',
        headers={
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        },
        json={
            'name': domain,
            'account': {'id': ACCOUNT_ID},
            'jump_start': True
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return {'domain': domain, 'success': True, 'zone_id': data['result']['id'], 'nameservers': data['result']['name_servers']}
        else:
            return {'domain': domain, 'success': False, 'error': data.get('errors')}
    else:
        return {'domain': domain, 'success': False, 'error': f'HTTP {response.status_code}'}

def create_dns_record(zone_id, domain):
    response = requests.post(
        f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records',
        headers={
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        },
        json={
            'type': 'A',
            'name': '@',
            'content': VDS_IP,
            'ttl': 3600,
            'proxied': True
        }
    )
    
    return response.status_code == 200

def main():
    print('Getting Porkbun-only domains...')
    domains = get_porkbun_only_domains()
    print(f'Found {len(domains)} Porkbun-only domains')
    
    results = []
    for i, domain in enumerate(domains, 1):
        print(f'[{i}/{len(domains)}] Creating zone for {domain}...')
        result = create_zone(domain)
        
        if result['success']:
            print(f'  Zone created: {result["zone_id"]}')
            print(f'  Nameservers: {result["nameservers"]}')
            
            dns_result = create_dns_record(result['zone_id'], domain)
            print(f'  DNS record created: {dns_result}')
            result['dns_record'] = dns_result
        else:
            print(f'  Failed: {result.get("error")}')
        
        results.append(result)
        time.sleep(1)  # Rate limiting
    
    with open(RESULTS, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f'\nResults saved to {RESULTS}')
    successful = sum(1 for r in results if r['success'])
    print(f'Successful: {successful}/{len(results)}')

if __name__ == '__main__':
    main()
