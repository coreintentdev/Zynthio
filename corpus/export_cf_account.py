#!/usr/bin/env python3
import requests
import json

TOKEN = 'cfut_f7VWf73WjPQeOjYvoElByJx184fFh9slVt99pkQt4fc7818c'
OUTPUT = '/root/zynthio/corpus/cloudflare_account2.txt'

def export_all_zones():
    page = 1
    per_page = 50
    all_zones = []
    
    while True:
        print(f'Fetching page {page}...')
        response = requests.get(
            f'https://api.cloudflare.com/client/v4/zones?page={page}&per_page={per_page}',
            headers={
                'Authorization': f'Bearer {TOKEN}',
                'Content-Type': 'application/json'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            zones = data.get('result', [])
            all_zones.extend(zones)
            
            total = data['result_info']['total_count']
            print(f'Found {len(zones)} zones on page {page} (total: {total})')
            
            if len(zones) < per_page:
                break
            
            page += 1
        else:
            print(f'Error: {response.status_code}')
            print(response.text)
            break
    
    print(f'Total zones exported: {len(all_zones)}')
    
    with open(OUTPUT, 'w') as f:
        for zone in all_zones:
            f.write(zone['name'].lower() + '\n')
    
    print(f'Saved to {OUTPUT}')

if __name__ == '__main__':
    export_all_zones()
