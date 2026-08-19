#!/usr/bin/env python3
import json
import sqlite3
import hashlib
from datetime import datetime

class AgentVerifier:
    """Agent verification system based on PhyAgentOS SessionVerifier
    for trust validation and failure recovery in Corey's stack
    """
    
    def __init__(self, db_path='/root/zynthio/governance/permissioned_ledger.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_verification_tables()
    
    def _create_verification_tables(self):
        """Create verification tables"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_time DATETIME,
            status TEXT DEFAULT 'active',
            operations_count INTEGER DEFAULT 0,
            success_count INTEGER DEFAULT 0,
            failure_count INTEGER DEFAULT 0
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_trust_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT NOT NULL,
            trust_score REAL DEFAULT 0.5,
            verification_count INTEGER DEFAULT 0,
            last_verified DATETIME DEFAULT CURRENT_TIMESTAMP,
            reliability_history TEXT
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS operation_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            operation_type TEXT NOT NULL,
            operation_data TEXT NOT NULL,
            result TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            verified BOOLEAN DEFAULT FALSE
        )
        ''')
        
        self.conn.commit()
    
    def start_session(self, agent_id):
        """Start a new agent session"""
        session_id = hashlib.md5(f'{agent_id}{datetime.utcnow().isoformat()}'.encode()).hexdigest()
        
        self.cursor.execute('''
        INSERT INTO agent_sessions (agent_id, session_id, status)
        VALUES (?, ?, 'active')
        ''', (agent_id, session_id))
        
        self.conn.commit()
        return session_id
    
    def end_session(self, session_id, success=True):
        """End an agent session"""
        status = 'completed' if success else 'failed'
        self.cursor.execute('''
        UPDATE agent_sessions 
        SET end_time = CURRENT_TIMESTAMP, status = ?
        WHERE session_id = ?
        ''', (status, session_id))
        self.conn.commit()
    
    def log_operation(self, session_id, operation_type, operation_data, result, verified=False):
        """Log an operation within a session"""
        self.cursor.execute('''
        INSERT INTO operation_log (session_id, operation_type, operation_data, result, verified)
        VALUES (?, ?, ?, ?, ?)
        ''', (session_id, operation_type, json.dumps(operation_data), json.dumps(result), verified))
        
        # Update session counters
        success = 1 if result.get('success', False) else 0
        failure = 0 if result.get('success', False) else 1
        
        self.cursor.execute('''
        UPDATE agent_sessions 
        SET operations_count = operations_count + 1,
            success_count = success_count + ?,
            failure_count = failure_count + ?
        WHERE session_id = ?
        ''', (success, failure, session_id))
        
        self.conn.commit()
    
    def verify_agent(self, agent_id):
        """Verify agent trust score"""
        self.cursor.execute('''
        SELECT trust_score, verification_count, reliability_history 
        FROM agent_trust_scores 
        WHERE agent_id = ?
        ''', (agent_id,))
        
        result = self.cursor.fetchone()
        if result:
            trust_score, verification_count, history = result
            reliability_history = json.loads(history) if history else []
        else:
            trust_score = 0.5
            verification_count = 0
            reliability_history = []
        
        # Calculate new trust score based on recent operations
        self.cursor.execute('''
        SELECT success_count, failure_count, operations_count 
        FROM agent_sessions 
        WHERE agent_id = ? AND end_time IS NOT NULL
        ORDER BY end_time DESC 
        LIMIT 10
        ''', (agent_id,))
        
        recent_sessions = self.cursor.fetchall()
        if recent_sessions:
            total_success = sum(session[0] for session in recent_sessions)
            total_failure = sum(session[1] for session in recent_sessions)
            total_ops = sum(session[2] for session in recent_sessions)
            
            if total_ops > 0:
                new_trust = (trust_score * 0.7) + ((total_success / total_ops) * 0.3)
                trust_score = round(new_trust, 3)
        
        # Update trust score
        self.cursor.execute('''
        INSERT OR REPLACE INTO agent_trust_scores (agent_id, trust_score, verification_count, last_verified, reliability_history)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
        ''', (agent_id, trust_score, verification_count + 1, json.dumps(reliability_history)))
        
        self.conn.commit()
        
        return {
            'agent_id': agent_id,
            'trust_score': trust_score,
            'verification_count': verification_count + 1,
            'verified_at': datetime.utcnow().isoformat()
        }
    
    def get_agent_status(self, agent_id):
        """Get comprehensive agent status"""
        # Get trust score
        self.cursor.execute('''
        SELECT trust_score, verification_count, last_verified 
        FROM agent_trust_scores 
        WHERE agent_id = ?
        ''', (agent_id,))
        
        trust_result = self.cursor.fetchone()
        
        # Get recent sessions
        self.cursor.execute('''
        SELECT session_id, start_time, end_time, status, operations_count, success_count, failure_count 
        FROM agent_sessions 
        WHERE agent_id = ? 
        ORDER BY start_time DESC 
        LIMIT 5
        ''', (agent_id,))
        
        sessions = []
        for row in self.cursor.fetchall():
            sessions.append({
                'session_id': row[0],
                'start_time': row[1],
                'end_time': row[2],
                'status': row[3],
                'operations_count': row[4],
                'success_count': row[5],
                'failure_count': row[6]
            })
        
        return {
            'agent_id': agent_id,
            'trust_score': trust_result[0] if trust_result else 0.5,
            'verification_count': trust_result[1] if trust_result else 0,
            'last_verified': trust_result[2] if trust_result else None,
            'recent_sessions': sessions
        }
    
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    verifier = AgentVerifier()
    
    # Test session management
    session_id = verifier.start_session('corey_twin_336')
    print(f'Started session: {session_id}')
    
    # Log some operations
    verifier.log_operation(session_id, 'creative_task', {'task': 'Secure holisticli.dev'}, {'success': True})
    verifier.log_operation(session_id, 'infra_check', {'check': 'disk_usage'}, {'success': True})
    verifier.log_operation(session_id, 'domain_purchase', {'domain': 'thatsonme.com'}, {'success': False})
    
    # End session
    verifier.end_session(session_id, success=True)
    
    # Verify agent
    verification = verifier.verify_agent('corey_twin_336')
    print(f'Agent verification: {verification}')
    
    # Get agent status
    status = verifier.get_agent_status('corey_twin_336')
    print(f'Agent status: {status}')
    
    verifier.close()
