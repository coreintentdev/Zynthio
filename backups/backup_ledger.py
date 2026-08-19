#!/usr/bin/env python3
import json
import sqlite3
from datetime import datetime
from pathlib import Path

def backup_ledger():
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path('/root/zynthio/backups')
    backup_file = backup_dir / f'ledger_backup_{timestamp}.json'
    
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect('/root/zynthio/governance/permissioned_ledger.db')
    cursor = conn.cursor()
    
    backup_data = {
        'timestamp': timestamp,
        'backup_type': 'full_ledger_backup',
        'tables': {}
    }
    
    tables = ['ledger_entries', 'twin_states', 'governance_proposals']
    for table in tables:
        cursor.execute(f'SELECT * FROM {table}')
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        backup_data['tables'][table] = {
            'columns': columns,
            'rows': [dict(zip(columns, row)) for row in rows]
        }
    
    conn.close()
    
    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, indent=2)
    
    backups = sorted(backup_dir.glob('ledger_backup_*.json'))
    if len(backups) > 10:
        for old_backup in backups[:-10]:
            old_backup.unlink()
    
    print(f'Ledger backup completed: {backup_file}')
    return backup_file

if __name__ == '__main__':
    backup_ledger()
