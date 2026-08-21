#!/usr/bin/env python3
import os
import json
import subprocess
from pathlib import Path

class DistributedCorpusCoordinator:
    def __init__(self, corpus_dir="/root/zynthio/corpus"):
        self.corpus_dir = Path(corpus_dir)
        self.nodes = [
            {'name': 'vds', 'ip': '100.64.0.2', 'role': 'master'},
            {'name': 'lilroblox', 'ip': '100.64.0.1', 'role': 'worker'},
            {'name': 'a07', 'ip': '100.64.0.4', 'role': 'backup'}
        ]
    
    def distribute_site_ranges(self, total_sites=806, num_workers=3):
        sites_per_worker = total_sites // num_workers
        ranges = []
        for i in range(num_workers):
            start = i * sites_per_worker
            end = (i + 1) * sites_per_worker if i < num_workers - 1 else total_sites
            ranges.append((start, end))
        return ranges
    
    def setup_workers(self):
        ranges = self.distribute_site_ranges()
        
        for i, node in enumerate(self.nodes):
            if node['role'] == 'master':
                continue
                
            start, end = ranges[i]
            config = {'worker_id': i, 'site_range': [start, end], 'master_ip': '100.64.0.2'}
            
            # Create corpus dir on worker
            subprocess.run(['ssh', 'root@' + node['ip'], 'mkdir -p /root/zynthio/corpus'])
            
            # Write config
            subprocess.run(['ssh', 'root@' + node['ip'], 'echo ' + json.dumps(config) + ' > /root/zynthio/corpus/worker_config.json'])
    
    def deploy_to_workers(self):
        self.setup_workers()
        
        for node in self.nodes:
            if node['role'] == 'master':
                continue
                
            print("Deploying corpus system to " + node['name'])
            subprocess.run(['rsync', '-avz', str(self.corpus_dir) + '/', 'root@' + node['ip'] + ':/root/zynthio/corpus/'])
    
    def start_parallel_ingestion(self):
        ranges = self.distribute_site_ranges()
        
        for i, node in enumerate(self.nodes):
            if node['role'] == 'master':
                continue
                
            start, end = ranges[i]
            config = {'worker_id': i, 'site_range': [start, end], 'master_ip': '100.64.0.2'}
            
            # Update config
            subprocess.run(['ssh', 'root@' + node['ip'], 'echo ' + json.dumps(config) + ' > /root/zynthio/corpus/worker_config.json'])
            
            print("Starting ingestion on " + node['name'] + " for sites " + str(start) + "-" + str(end))
            subprocess.run(['ssh', 'root@' + node['ip'], 'cd /root/zynthio/corpus && source venv/bin/activate && python scale_ingest_worker.py'])

if __name__ == "__main__":
    coordinator = DistributedCorpusCoordinator()
    coordinator.deploy_to_workers()
    coordinator.start_parallel_ingestion()