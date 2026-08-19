#!/usr/bin/env python3
import os
import json
from datetime import datetime
from pathlib import Path

class WhatsAppMonitor:
    def __init__(self):
        self.signal = 336
        self.whatsapp_dir = Path('/root/zynthio/inbox/whatsapp')
        self.digest_dir = Path('/root/zynthio/_meta/mail_digest')
        self.digest_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = Path('/root/zynthio/.whatsapp_monitor_state.json')
        
    def get_latest_whatsapp_data(self):
        try:
            # Get the latest extract file
            extract_files = sorted(self.whatsapp_dir.glob('mac_extract_*.json'))
            if not extract_files:
                return {'status': 'no_data', 'message': 'No WhatsApp extract files found'}
            
            latest_file = extract_files[-1]
            extract_data = json.loads(latest_file.read_text())
            
            # Get the main JSONL file
            jsonl_file = self.whatsapp_dir / 'mac_chatstorage_all_messages.jsonl'
            if not jsonl_file.exists():
                return {'status': 'no_jsonl', 'message': 'No WhatsApp JSONL file found'}
            
            # Count messages
            message_count = 0
            with open(jsonl_file, 'r') as f:
                for line in f:
                    message_count += 1
            
            return {
                'status': 'success',
                'latest_extract': str(latest_file.name),
                'extract_timestamp': extract_data.get('utc'),
                'total_messages': message_count,
                'sessions': extract_data.get('sessions'),
                'messages_with_text': extract_data.get('messages_with_text'),
                'source_db': extract_data.get('source_db')
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def get_recent_messages(self, limit=10):
        try:
            jsonl_file = self.whatsapp_dir / 'mac_chatstorage_all_messages.jsonl'
            if not jsonl_file.exists():
                return []
            
            recent_messages = []
            with open(jsonl_file, 'r') as f:
                for line in f:
                    if len(recent_messages) >= limit:
                        break
                    try:
                        msg = json.loads(line)
                        recent_messages.append(msg)
                    except:
                        continue
            
            return recent_messages
        except Exception as e:
            return []
    
    def check_sync_status(self):
        try:
            extract_files = list(self.whatsapp_dir.glob('mac_extract_*.json'))
            if not extract_files:
                return {'status': 'no_sync', 'last_sync': None}
            
            latest_file = max(extract_files, key=lambda f: f.stat().st_mtime)
            last_sync_time = datetime.fromtimestamp(latest_file.stat().st_mtime)
            
            # Check if sync is recent (within 1 hour)
            time_diff = datetime.now() - last_sync_time
            is_recent = time_diff.total_seconds() < 3600
            
            return {
                'status': 'synced' if is_recent else 'stale',
                'last_sync': last_sync_time.isoformat(),
                'time_diff_hours': time_diff.total_seconds() / 3600,
                'latest_file': latest_file.name
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def generate_whatsapp_report(self):
        report = {
            'signal': self.signal,
            'timestamp': datetime.utcnow().isoformat(),
            'monitor_status': 'automated',
            'sync_status': self.check_sync_status(),
            'whatsapp_data': self.get_latest_whatsapp_data(),
            'recent_messages': self.get_recent_messages(5),
            'recommendations': [
                'WhatsApp monitoring operational via Mac sync',
                'Messages extracted from Mac ChatStorage.sqlite',
                'Ensure Mac WhatsApp sync runs regularly for real-time data'
            ]
        }
        
        report_file = self.digest_dir / 'WHATSAPP_MONITOR_REPORT.json'
        report_file.write_text(json.dumps(report, indent=2))
        
        state = {
            'last_check': datetime.utcnow().isoformat(),
            'last_sync': report['sync_status'].get('last_sync'),
            'total_messages': report['whatsapp_data'].get('total_messages', 0)
        }
        self.state_file.write_text(json.dumps(state, indent=2))
        
        return report
    
    def run_automated_check(self):
        print('WhatsApp Automated Check')
        print('Signal:', self.signal)
        
        report = self.generate_whatsapp_report()
        
        print('Status:', report['whatsapp_data']['status'])
        print('Total Messages:', report['whatsapp_data'].get('total_messages', 0))
        print('Sync Status:', report['sync_status']['status'])
        print('Last Sync:', report['sync_status'].get('last_sync', 'unknown'))
        
        return report

if __name__ == '__main__':
    monitor = WhatsAppMonitor()
    report = monitor.run_automated_check()
    
    if report['whatsapp_data']['status'] == 'success':
        exit(0)
    else:
        exit(1)
