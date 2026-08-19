#!/usr/bin/env python3
import json
import sqlite3
from datetime import datetime

class TRIDENTScoring:
    """TRIDENT governance implementation for Corey's stack
    Based on ATLAS architecture from gdtsitlauri/atlas-trident
    
    Scoring Factors:
    T - Trust: Source credibility
    R - Relevance: Alignment with creative intent  
    I - Impact: Potential value
    D - Deadline: Time sensitivity
    E - Execution: Resource requirements
    N - Novelty: Innovation factor
    T - Timing: Current context alignment
    """
    
    def __init__(self, db_path='/root/zynthio/governance/permissioned_ledger.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def calculate_trident_score(self, task_data):
        """Calculate composite TRIDENT score for a task
        
        Args:
            task_data: dict with task information
            
        Returns:
            float: TRIDENT score (0.0 to 1.0)
        """
        # Trust factor
        source = task_data.get('source', 'agent')
        if source == 'corey_direct':
            trust = 1.0
        elif source == 'agent_suggestion':
            trust = 0.7
        elif source == 'infra_alert':
            trust = 0.3
        else:
            trust = 0.5
        
        # Relevance factor
        cluster = task_data.get('cluster', 'infra')
        if cluster == 'creative':
            relevance = 1.0
        elif cluster == 'infra':
            relevance = 0.4
        else:
            relevance = 0.6
        
        # Impact factor
        priority = task_data.get('priority', 5)
        if priority == 0:
            impact = 1.0
        elif priority <= 2:
            impact = 0.8
        elif priority <= 4:
            impact = 0.5
        else:
            impact = 0.2
        
        # Deadline factor
        urgency = task_data.get('urgency', 'normal')
        if urgency == 'urgent':
            deadline = 1.0
        elif urgency == 'normal':
            deadline = 0.5
        else:
            deadline = 0.3
        
        # Execution factor
        resource_cost = task_data.get('resource_cost', 'medium')
        if resource_cost == 'low':
            execution = 1.0
        elif resource_cost == 'medium':
            execution = 0.6
        else:
            execution = 0.3
        
        # Novelty factor
        is_new = task_data.get('is_new', False)
        if is_new:
            novelty = 1.0
        else:
            novelty = 0.4
        
        # Timing factor
        timing = task_data.get('timing', 'now')
        if timing == 'now':
            timing_score = 1.0
        elif timing == 'soon':
            timing_score = 0.6
        else:
            timing_score = 0.3
        
        # Calculate composite score
        trident_score = (trust + relevance + impact + deadline + execution + novelty + timing_score) / 7
        
        return round(trident_score, 3)
    
    def score_and_log_task(self, task_data):
        """Score a task and log it to the permissioned ledger
        
        Args:
            task_data: dict with task information
            
        Returns:
            dict: Scored task with TRIDENT score
        """
        score = self.calculate_trident_score(task_data)
        task_data['trident_score'] = score
        task_data['scored_at'] = datetime.utcnow().isoformat()
        
        # Log to ledger
        self.cursor.execute('''
        INSERT INTO ledger_entries (entry_type, entry_data, status, validator)
        VALUES (?, ?, ?, ?)
        ''', ('task_scored', json.dumps(task_data), 'validated', 'TRIDENT'))
        
        self.conn.commit()
        
        return task_data
    
    def get_priority_recommendation(self, score):
        """Get priority recommendation based on TRIDENT score
        
        Args:
            score: TRIDENT score (0.0 to 1.0)
            
        Returns:
            str: Priority recommendation
        """
        if score >= 0.8:
            return 'P0'
        elif score >= 0.6:
            return 'P1'
        elif score >= 0.4:
            return 'P2'
        else:
            return 'P3'
    
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    # Test the scoring system
    scorer = TRIDENTScoring()
    
    # Test creative task
    creative_task = {
        'task': 'Secure domain: holisticli.dev',
        'source': 'corey_direct',
        'cluster': 'creative',
        'priority': 0,
        'urgency': 'urgent',
        'resource_cost': 'low',
        'is_new': True,
        'timing': 'now'
    }
    
    scored_creative = scorer.score_and_log_task(creative_task)
    print(f'Creative Task Score: {scored_creative["trident_score"]}')
    print(f'Priority: {scorer.get_priority_recommendation(scored_creative["trident_score"])}')
    
    # Test infra task
    infra_task = {
        'task': 'Check VDS capacity',
        'source': 'infra_alert',
        'cluster': 'infra',
        'priority': 1,
        'urgency': 'normal',
        'resource_cost': 'low',
        'is_new': False,
        'timing': 'now'
    }
    
    scored_infra = scorer.score_and_log_task(infra_task)
    print(f'Infra Task Score: {scored_infra["trident_score"]}')
    print(f'Priority: {scorer.get_priority_recommendation(scored_infra["trident_score"])}')
    
    scorer.close()
