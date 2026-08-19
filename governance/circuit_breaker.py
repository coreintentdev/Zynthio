#!/usr/bin/env python3
import json
import sqlite3
import time
from datetime import datetime, timedelta
from enum import Enum

class CircuitState(Enum):
    CLOSED = 'closed'      # Normal operation
    OPEN = 'open'          # Circuit broken, reject calls
    HALF_OPEN = 'half_open'  # Testing if service recovered

class CircuitBreaker:
    """Circuit breaker for API dependency isolation"""
    
    def __init__(self, db_path='/root/zynthio/governance/permissioned_ledger.db'):
        self.db_path = db_path
        self.failure_threshold = 3
        self.success_threshold = 2
        self.timeout = 60  # seconds
        self.circuit_state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self._load_state()
    
    def _load_state(self):
        """Load circuit breaker state from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT entry_data FROM ledger_entries WHERE entry_type = "circuit_breaker_state" ORDER BY timestamp DESC LIMIT 1')
        row = cursor.fetchone()
        
        if row:
            state_data = json.loads(row[0])
            self.circuit_state = CircuitState(state_data['state'])
            self.failure_count = state_data['failure_count']
            self.success_count = state_data['success_count']
            self.last_failure_time = datetime.fromisoformat(state_data['last_failure_time']) if state_data['last_failure_time'] else None
        
        conn.close()
    
    def _save_state(self):
        """Save circuit breaker state to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        state_data = {
            'state': self.circuit_state.value,
            'failure_count': self.failure_count,
            'success_count': self.success_count,
            'last_failure_time': self.last_failure_time.isoformat() if self.last_failure_time else None,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        cursor.execute('INSERT INTO ledger_entries (entry_type, entry_data, status, validator) VALUES (?, ?, ?, ?)',
                       ('circuit_breaker_state', json.dumps(state_data), 'validated', 'CIRCUIT_BREAKER'))
        
        conn.commit()
        conn.close()
    
    def call_allowed(self):
        """Check if API call is allowed based on circuit state"""
        if self.circuit_state == CircuitState.CLOSED:
            return True, 'Circuit closed - calls allowed'
        
        if self.circuit_state == CircuitState.OPEN:
            if self.last_failure_time and (datetime.utcnow() - self.last_failure_time) > timedelta(seconds=self.timeout):
                self.circuit_state = CircuitState.HALF_OPEN
                self._save_state()
                return True, 'Circuit half-open - testing recovery'
            return False, 'Circuit open - calls blocked'
        
        if self.circuit_state == CircuitState.HALF_OPEN:
            return True, 'Circuit half-open - testing recovery'
        
        return False, 'Unknown circuit state'
    
    def record_success(self):
        """Record successful API call"""
        if self.circuit_state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.circuit_state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        elif self.circuit_state == CircuitState.CLOSED:
            self.failure_count = 0
        
        self._save_state()
    
    def record_failure(self):
        """Record failed API call"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        self.success_count = 0
        
        if self.failure_count >= self.failure_threshold:
            self.circuit_state = CircuitState.OPEN
        
        self._save_state()
    
    def get_status(self):
        """Get current circuit breaker status"""
        return {
            'state': self.circuit_state.value,
            'failure_count': self.failure_count,
            'success_count': self.success_count,
            'last_failure_time': self.last_failure_time.isoformat() if self.last_failure_time else None,
            'threshold': self.failure_threshold,
            'timeout': self.timeout
        }

if __name__ == '__main__':
    breaker = CircuitBreaker()
    
    print('Circuit Breaker Status:')
    status = breaker.get_status()
    print(f'State: {status["state"].upper()}')
    print(f'Failures: {status["failure_count"]}/{status["threshold"]}')
    print(f'Successes: {status["success_count"]}')
    print(f'Last Failure: {status["last_failure_time"]}')
    
    allowed, message = breaker.call_allowed()
    print(f'Call Allowed: {allowed} - {message}')
