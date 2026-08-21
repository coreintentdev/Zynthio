#!/usr/bin/env python3
"""
Run this on your MacBook to export Porkbun domains
Requires: python3 requests
"""

import requests
import json

API_KEY = 'pk1_6f31c072da949de78af42a38e0e6a2f12d509c4fc04cb638a263f437130a1a7a'
SECRET_KEY = 'sk1_9f6bc019b58fd3fa5a20407d4293031149ced68e493f71d80599ee6ffb311399'

def get_all_domains():
    url = 'https://api.porkbun.com/api/json/v3/domain/listAll'
    headers = {
        'X-API-Key': API_KEY,
        'X-Secret-API-Key': SECRET_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json={}, headers=headers, timeout=30)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'SUCCESS':
                domains = data.get('domains', [])
                print(f'Found {len(domains)} domains')
                return domains
            else:
                print(f'API Error: {data.get("status")}')
                return []
        else:
            print(f'HTTP Error: {response.status_code}')
            print(f'Response: {response.text[:200]}')
            return []
    except Exception as e:
        print(f'Exception: {e}')
        return []

if __name__ == '__main__':
    domains = get_all_domains()
    
    if domains:
        with open('porkbun_domains.txt', 'w') as f:
            for domain in domains:
                # Handle both string and dict formats
                if isinstance(domain, dict):
                    domain_name = domain.get('domain', domain.get('name', str(domain)))
                else:
                    domain_name = str(domain)
                f.write(domain_name.lower() + '\n')
        print(f'Saved {len(domains)} domains to porkbun_domains.txt')
        
        # Also save as JSON for backup
        with open('porkbun_domains.json', 'w') as f:
            json.dump(domains, f, indent=2)
        print(f'Saved {len(domains)} domains to porkbun_domains.json')
    else:
        print('No domains retrieved')