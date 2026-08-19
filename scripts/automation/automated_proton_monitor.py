#!/usr/bin/env python3
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class ProtonEmailMonitor:
    def __init__(self):
        self.signal = 336
        self.config_path = Path('/root/.zynthio.env')
        self.digest_dir = Path('/root/zynthio/_meta/mail_digest')
        self.digest_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = Path('/root/zynthio/.proton_monitor_state.json')
        
    def fallback_tutanota_monitor(self):
        try:
            latest_digest = self.digest_dir / 'EMAIL_DIGEST_latest.md'
            if not latest_digest.exists():
                return {'status': 'no_digest', 'proton_emails': 0}
            
            content = latest_digest.read_text()
            proton_emails = content.count('From: Proton <no-reply@mail.proton.me>')
            
            return {
                'status': 'success',
                'method': 'tutanota_fallback',
                'proton_emails': proton_emails,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def check_bridge_status(self):
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', 'proton-mail-bridge.service'],
                capture_output=True, text=True, timeout=5
            )
            return {
                'status': result.stdout.strip(),
                'recoverable': result.returncode == 0
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def generate_proton_report(self):
        report = {
            'signal': self.signal,
            'timestamp': datetime.utcnow().isoformat(),
            'monitor_status': 'automated',
            'bridge_status': self.check_bridge_status(),
            'email_data': self.fallback_tutanota_monitor(),
            'recommendations': [
                'Proton Bridge broken on VDS (headless Qt issues)',
                'Using Tutanota fallback - Proton notifications forwarded there',
                'Consider setting up Proton API for direct access'
            ]
        }
        
        report_file = self.digest_dir / 'PROTON_MONITOR_REPORT.json'
        report_file.write_text(json.dumps(report, indent=2))
        
        state = {
            'last_check': datetime.utcnow().isoformat(),
            'last_status': report['email_data']['status'],
            'proton_email_count': report['email_data'].get('proton_emails', 0)
        }
        self.state_file.write_text(json.dumps(state, indent=2))
        
        return report
    
    def run_automated_check(self):
        print('Proton Email Automated Check')
        print('Signal:', self.signal)
        
        report = self.generate_proton_report()
        
        print('Status:', report['email_data']['status'])
        print('Method:', report['email_data'].get('method', 'unknown'))
        print('Proton Emails Found:', report['email_data'].get('proton_emails', 0))
        
        return report

if __name__ == '__main__':
    monitor = ProtonEmailMonitor()
    report = monitor.run_automated_check()
    
    if report['email_data']['status'] == 'success':
        exit(0)
    else:
        exit(1)
