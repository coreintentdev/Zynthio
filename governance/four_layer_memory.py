#!/usr/bin/env python3
import json
import sqlite3
from datetime import datetime
from collections import defaultdict

class FourLayerMemory:
    def __init__(self, db_path='/root/zynthio/governance/permissioned_ledger.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_memory_tables()
        self.working_memory = defaultdict(list)
    
    def _create_memory_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS episodic_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT NOT NULL,
            event_data TEXT NOT NULL,
            context TEXT,
            importance REAL DEFAULT 0.5,
            access_count INTEGER DEFAULT 0
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS semantic_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept TEXT NOT NULL,
            concept_data TEXT NOT NULL,
            category TEXT,
            confidence REAL DEFAULT 0.8,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS procedural_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL,
            procedure_data TEXT NOT NULL,
            success_rate REAL DEFAULT 0.0,
            usage_count INTEGER DEFAULT 0,
            last_used DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.conn.commit()
    
    def add_working_memory(self, layer, data):
        self.working_memory[layer].append({
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        })
        if len(self.working_memory[layer]) > 10:
            self.working_memory[layer].pop(0)
    
    def add_episodic_memory(self, event_type, event_data, context=None, importance=0.5):
        self.cursor.execute('''
        INSERT INTO episodic_memory (event_type, event_data, context, importance)
        VALUES (?, ?, ?, ?)
        ''', (event_type, json.dumps(event_data), json.dumps(context) if context else None, importance))
        self.conn.commit()
    
    def add_semantic_memory(self, concept, concept_data, category=None, confidence=0.8):
        self.cursor.execute('''
        INSERT INTO semantic_memory (concept, concept_data, category, confidence)
        VALUES (?, ?, ?, ?)
        ''', (concept, json.dumps(concept_data), category, confidence))
        self.conn.commit()
    
    def add_procedural_memory(self, skill_name, procedure_data):
        self.cursor.execute('''
        INSERT INTO procedural_memory (skill_name, procedure_data)
        VALUES (?, ?)
        ''', (skill_name, json.dumps(procedure_data)))
        self.conn.commit()
    
    def update_procedural_success(self, skill_name, success):
        self.cursor.execute('''
        UPDATE procedural_memory 
        SET success_rate = (success_rate * usage_count + ?) / (usage_count + 1),
            usage_count = usage_count + 1,
            last_used = CURRENT_TIMESTAMP
        WHERE skill_name = ?
        ''', (1.0 if success else 0.0, skill_name))
        self.conn.commit()
    
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    memory = FourLayerMemory()
    memory.add_working_memory('creative_queue', {'task': 'Secure holisticli.dev', 'priority': 'P0'})
    memory.add_episodic_memory('domain_purchase', {'domain': 'holisticli.dev', 'action': 'purchase_initiated'}, importance=0.9)
    memory.add_semantic_memory('holistic_ai', {'definition': 'AI that considers entire context'}, category='philosophy')
    memory.add_procedural_memory('creative_priority_override', {'script': '/root/zynthio/scripts/creative_priority_override.py'})
    memory.update_procedural_success('creative_priority_override', True)
    print('Four-layer memory system test complete')
    memory.close()
