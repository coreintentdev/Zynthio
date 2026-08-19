#!/usr/bin/env python3
import json
import re
import sys
sys.path.append('/root/zynthio/governance')
from trident_scoring import TRIDENTScoring
from four_layer_memory import FourLayerMemory
from agent_verification import AgentVerifier
from policy_guard import PolicyGuard
from datetime import datetime

def enhanced_creative_priority_override():
    scorer = TRIDENTScoring()
    memory = FourLayerMemory()
    verifier = AgentVerifier()
    guard = PolicyGuard()
    
    session_id = verifier.start_session('creative_priority_override_agent')
    
    try:
        with open('/root/zynthio/BUILD_STACK_QUEUE_LIVE.json', 'r') as f:
            queue = json.load(f)
        
        with open('/root/zynthio-tools/zynthio/COREY_CREATIVE_LEDGER.md', 'r') as f:
            ledger = f.read()
        
        memory.add_working_memory('queue_status', {
            'total_tasks': len(queue.get('hermes_ingest', [])),
            'creative_tasks': 0
        })
        
        creative_tasks = []
        
        song_pattern = r'##\s*(\d+)\s+([^\n]+)'
        songs = re.findall(song_pattern, ledger)
        for num, title in songs:
            task_data = {
                'task': f'Process song: {title}',
                'source': 'corey_direct',
                'cluster': 'creative',
                'priority': 0,
                'urgency': 'urgent',
                'resource_cost': 'low',
                'is_new': True,
                'timing': 'now'
            }
            
            scored_task = scorer.score_and_log_task(task_data)
            creative_tasks.append(scored_task)
            
            memory.add_episodic_memory('song_task', {
                'song': title,
                'number': num,
                'trident_score': scored_task['trident_score']
            }, importance=0.8)
        
        domain_pattern = r'\*\*(.*?)\*\*\s*—\s*([^\n]+)'
        domains = re.findall(domain_pattern, ledger)
        for domain, desc in domains:
            if domain.endswith('.com') or domain.endswith('.dev') or domain.endswith('.net'):
                task_data = {
                    'task': f'Secure domain: {domain}',
                    'source': 'corey_direct',
                    'cluster': 'creative',
                    'priority': 0,
                    'urgency': 'urgent',
                    'resource_cost': 'medium',
                    'is_new': True,
                    'timing': 'now'
                }
                
                scored_task = scorer.score_and_log_task(task_data)
                policy_result = guard.check_operation(scored_task)
                
                if policy_result['allowed']:
                    creative_tasks.append(scored_task)
                    
                    memory.add_episodic_memory('domain_task', {
                        'domain': domain,
                        'description': desc,
                        'trident_score': scored_task['trident_score']
                    }, importance=0.9)
                else:
                    print(f'Policy violation for domain {domain}: {policy_result["violations"]}')
        
        if 'digital twin' in ledger.lower():
            task_data = {
                'task': 'Continue digital twin development (336 signal)',
                'source': 'corey_direct',
                'cluster': 'creative',
                'priority': 0,
                'urgency': 'urgent',
                'resource_cost': 'medium',
                'is_new': False,
                'timing': 'now'
            }
            
            scored_task = scorer.score_and_log_task(task_data)
            creative_tasks.append(scored_task)
            
            memory.add_semantic_memory('digital_twin_336', {
                'signal': 336,
                'description': 'Core digital twin development',
                'trident_score': scored_task['trident_score']
            }, category='core_concept')
        
        creative_tasks.sort(key=lambda x: x['trident_score'], reverse=True)
        
        queue['build_order'] = creative_tasks + queue['build_order']
        
        if 'hermes_suggested_tasks' not in queue:
            queue['hermes_suggested_tasks'] = []
        
        for task in creative_tasks:
            queue['hermes_suggested_tasks'].insert(0, {
                'task': task['task'],
                'priority': scorer.get_priority_recommendation(task['trident_score']),
                'cluster': task['cluster'],
                'trident_score': task['trident_score'],
                'from': 'ENHANCED_CREATIVE_PRIORITY_OVERRIDE',
                'added': task['scored_at']
            })
        
        with open('/root/zynthio/BUILD_STACK_QUEUE_LIVE.json', 'w') as f:
            json.dump(queue, f, indent=2)
        
        verifier.log_operation(session_id, 'creative_priority_override', {
            'tasks_processed': len(creative_tasks),
            'average_trident_score': sum(t['trident_score'] for t in creative_tasks) / len(creative_tasks) if creative_tasks else 0
        }, {'success': True}, verified=True)
        
        memory.add_procedural_memory('enhanced_creative_override', {
            'description': 'Enhanced creative priority override with full governance',
            'governance_components': ['TRIDENT', 'four_layer_memory', 'agent_verification', 'policy_guard']
        })
        memory.update_procedural_success('enhanced_creative_override', True)
        
        print(f'Enhanced override complete: {len(creative_tasks)} creative tasks processed with full governance')
        print(f'Average TRIDENT score: {sum(t["trident_score"] for t in creative_tasks) / len(creative_tasks) if creative_tasks else 0:.3f}')
        
        verifier.end_session(session_id, success=True)
        
        verification = verifier.verify_agent('creative_priority_override_agent')
        print(f'Agent trust score: {verification["trust_score"]}')
        
    except Exception as e:
        verifier.log_operation(session_id, 'creative_priority_override', {
            'error': str(e)
        }, {'success': False}, verified=True)
        verifier.end_session(session_id, success=False)
        memory.update_procedural_success('enhanced_creative_override', False)
        raise
    
    finally:
        scorer.close()
        memory.close()
        verifier.close()
        guard.close()

if __name__ == '__main__':
    enhanced_creative_priority_override()
