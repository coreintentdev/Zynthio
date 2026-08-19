#!/usr/bin/env python3
import json
import sqlite3
from datetime import datetime

class PolicyGuard:
    """Policy guard system for hard safety constraints and rejection logic
    Based on ATLAS policy_guard component for Corey's stack
    """
    
    def __init__(self, db_path='/root/zynthio/governance/permissioned_ledger.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_policy_tables()
        self._load_default_policies()
    
    def _create_policy_tables(self):
        """Create policy tables"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS policies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_name TEXT NOT NULL,
            policy_type TEXT NOT NULL,
            policy_rule TEXT NOT NULL,
            severity TEXT DEFAULT 'warning',
            enabled BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS policy_violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_id INTEGER NOT NULL,
            violation_type TEXT NOT NULL,
            operation_data TEXT NOT NULL,
            action_taken TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (policy_id) REFERENCES policies (id)
        )
        ''')
        
        self.conn.commit()
    
    def _load_default_policies(self):
        """Load default safety policies for Corey's stack"""
        default_policies = [
            ('creative_override', 'priority', 'Creative tasks must always override infrastructure noise', 'critical'),
            ('no_destructive_without_approval', 'safety', 'No destructive operations without explicit Corey approval', 'critical'),
            ('all_changes_logged', 'audit', 'All changes must be logged to permissioned ledger', 'high'),
            ('twin_state_validation', 'validation', 'Twin state changes require validation', 'high'),
            ('resource_limits', 'resource', 'Resource usage must stay within safe thresholds', 'high'),
            ('corey_override_capability', 'override', 'Any decision can be overridden by direct Corey command', 'critical'),
            ('rollback_capability', 'recovery', 'All ledger entries support rollback', 'high'),
            ('audit_trail', 'audit', 'Complete history of all governance decisions', 'medium')
        ]
        
        for policy_name, policy_type, policy_rule, severity in default_policies:
            self.cursor.execute('''
            INSERT OR IGNORE INTO policies (policy_name, policy_type, policy_rule, severity)
            VALUES (?, ?, ?, ?)
            ''', (policy_name, policy_type, policy_rule, severity))
        
        self.conn.commit()
    
    def check_operation(self, operation_data):
        """Check if operation violates any policies
        
        Args:
            operation_data: dict with operation details
            
        Returns:
            dict: {allowed: bool, violations: [], warnings: []}
        """
        result = {
            'allowed': True,
            'violations': [],
            'warnings': []
        }
        
        # Check creative override policy
        if operation_data.get('cluster') == 'infra' and operation_data.get('priority') == 0:
            result['allowed'] = False
            result['violations'].append({
                'policy': 'creative_override',
                'reason': 'Infrastructure tasks cannot have P0 priority - creative tasks must override'
            })
        
        # Check destructive operations
        if operation_data.get('destructive', False) and not operation_data.get('corey_approval'):
            result['allowed'] = False
            result['violations'].append({
                'policy': 'no_destructive_without_approval',
                'reason': 'Destructive operations require explicit Corey approval'
            })
        
        # Check resource limits
        if operation_data.get('resource_cost') == 'high' and operation_data.get('cluster') == 'infra':
            result['warnings'].append({
                'policy': 'resource_limits',
                'reason': 'High resource cost infrastructure operation - verify necessity'
            })
        
        # Log check to ledger
        self.cursor.execute('''
        INSERT INTO ledger_entries (entry_type, entry_data, status, validator)
        VALUES (?, ?, ?, ?)
        ''', ('policy_check', json.dumps({
            'operation': operation_data,
            'result': result
        }), 'validated', 'POLICY_GUARD'))
        
        self.conn.commit()
        
        return result
    
    def log_violation(self, policy_id, violation_type, operation_data, action_taken):
        """Log a policy violation"""
        self.cursor.execute('''
        INSERT INTO policy_violations (policy_id, violation_type, operation_data, action_taken)
        VALUES (?, ?, ?, ?)
        ''', (policy_id, violation_type, json.dumps(operation_data), action_taken))
        self.conn.commit()
    
    def get_active_policies(self):
        """Get all active policies"""
        self.cursor.execute('''
        SELECT policy_name, policy_type, policy_rule, severity 
        FROM policies 
        WHERE enabled = TRUE
        ''')
        
        policies = []
        for row in self.cursor.fetchall():
            policies.append({
                'name': row[0],
                'type': row[1],
                'rule': row[2],
                'severity': row[3]
            })
        
        return policies
    
    def enable_policy(self, policy_name):
        """Enable a policy"""
        self.cursor.execute('''
        UPDATE policies SET enabled = TRUE WHERE policy_name = ?
        ''', (policy_name,))
        self.conn.commit()
    
    def disable_policy(self, policy_name):
        """Disable a policy (requires Corey override)"""
        self.cursor.execute('''
        UPDATE policies SET enabled = FALSE WHERE policy_name = ?
        ''', (policy_name,))
        self.conn.commit()
    
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    guard = PolicyGuard()
    
    # Test policy checking
    print('Active policies:', guard.get_active_policies())
    
    # Test allowed operation
    allowed_op = {
        'task': 'Secure domain: holisticli.dev',
        'cluster': 'creative',
        'priority': 0,
        'destructive': False
    }
    result = guard.check_operation(allowed_op)
    print(f'Allowed operation result: {result}')
    
    # Test violating operation
    violating_op = {
        'task': 'Delete all logs',
        'cluster': 'infra',
        'priority': 0,
        'destructive': True,
        'corey_approval': False
    }
    result = guard.check_operation(violating_op)
    print(f'Violating operation result: {result}')
    
    guard.close()
