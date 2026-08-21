#!/usr/bin/env python3
import requests
import json

API_KEY = 'pk1_6f31c072da949de78af42a38e0e6a2f12d509c4fc04cb638a263f437130a1a7a'
SECRET_KEY = 'sk1_9f6bc019b58fd3fa5a20407d4293031149ced68e493f71d80599ee6ffb311399'

def get_all_domains():
    domains = []
    page = 1
    per_page = 100
    
    while True:
        headers = {
            'X-API-Key': API_KEY,
            'X-Secret-API-Key': SECRET_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://api.porkbun.com/api/json/v3/domain/listAll',
            json={},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'SUCCESS':
                domains.extend(data.get('domains', []))
                if len(data.get('domains', [])) < per_page:
                    break
                page += 1
            else:
                print('Error:', data.get('status'))
                break
        else:
            print('HTTP Error:', response.status_code)
            break
    
    return domains

if __name__ == '__main__':
    domains = get_all_domains()
    print(f'Total domains: {len(domains)}')
    
    with open('/tmp/porkbun_domains.txt', 'w') as f:
        for domain in domains:
            # Handle both string and dict formats
            if isinstance(domain, dict):
                domain_name = domain.get('domain', domain.get('name', str(domain)))
            else:
                domain_name = str(domain)
            f.write(domain_name.lower() + '\n')
    
    print('Saved to /tmp/porkbun_domains.txt')
