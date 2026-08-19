#!/usr/bin/env python3
import subprocess
import time
import json
import sqlite3
from datetime import datetime
from pathlib import Path

class ProcessWatchdog:
    """Watchdog for monitoring and restarting critical processes"""
    
    def __init__(self, db_path='/root/zynthio/governance/permissioned_ledger.db'):
        self.db_path = db_path
        self.monitored_processes = {
            'creative_priority_override': {
                'script': '/root/zynthio/scripts/enhanced_creative_priority_override.py',
                'expected_interval': 86400,  # 24 hours
                'last_run': None,
                'max_restarts': 3,
                'restart_count': 0
            }
        }
    
    def check_process_health(self, process_name):
        """Check if a process is healthy"""
        process_info = self.monitored_processes.get(process_name)
        if not process_info:
            return False, 'Process not monitored'
        
        # Check if script exists
        if not Path(process_info['script']).exists():
            return False, f'Script not found: {process_info["script"]}'
        
        # Check last run time from logs
        log_file = Path('/root/zynthio/logs/creative_priority.log')
        if log_file.exists():
            # Get last modification time
            last_modified = datetime.fromtimestamp(log_file.stat().st_mtime)
            time_since_run = (datetime.utcnow() - last_modified).total_seconds()
            
            if time_since_run > process_info['expected_interval'] * 1.5:  # 50% buffer
                return False, f'Process overdue: {time_since_run:.0f}s since last run'
        
        return True, 'Process healthy'
    
    def restart_process(self, process_name):
        """Restart a failed process"""
        process_info = self.monitored_processes.get(process_name)
        if not process_info:
            return False, 'Process not monitored'
        
        if process_info['restart_count'] >= process_info['max_restarts']:
            return False, f'Max restarts reached: {process_info["max_restarts"]}'
        
        try:
            # Run the process
            result = subprocess.run(
                ['python3', process_info['script']],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            process_info['restart_count'] += 1
            process_info['last_run'] = datetime.utcnow().isoformat()
            
            if result.returncode == 0:
                return True, f'Process restarted successfully (attempt {process_info["restart_count"]})'
            else:
                return False, f'Process restart failed: {result.stderr}'
        
        except subprocess.TimeoutExpired:
            return False, 'Process restart timed out'
        except Exception as e:
            return False, f'Process restart error: {str(e)}'
    
    def log_health_check(self, process_name, healthy, message):
        """Log health check result to ledger"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO ledger_entries (entry_type, entry_data, status, validator)
        VALUES (?, ?, ?, ?)
        ''', ('health_check', json.dumps({
            'process': process_name,
            'healthy': healthy,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }), 'validated', 'WATCHDOG'))
        
        conn.commit()
        conn.close()
    
    def run_health_checks(self):
        """Run health checks on all monitored processes"""
        results = {}
        
        for process_name in self.monitored_processes:
            healthy, message = self.check_process_health(process_name)
            results[process_name] = {
                'healthy': healthy,
                'message': message,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Log to ledger
            self.log_health_check(process_name, healthy, message)
            
            # Restart if unhealthy
            if not healthy:
                restart_success, restart_message = self.restart_process(process_name)
                results[process_name]['restart_attempted'] = True
                results[process_name]['restart_success'] = restart_success
                results[process_name]['restart_message'] = restart_message
        
        return results

if __name__ == '__main__':
    watchdog = ProcessWatchdog()
    results = watchdog.run_health_checks()
    
    print('Watchdog Health Check Results:')
    for process_name, result in results.items():
        status = '✓ HEALTHY' if result['healthy'] else '✗ UNHEALTHY'
        print(f'{process_name}: {status} - {result["message"]}')
        
        if result.get('restart_attempted'):
            restart_status = '✓ SUCCESS' if result['restart_success'] else '✗ FAILED'
            print(f'  Restart: {restart_status} - {result["restart_message"]}')
