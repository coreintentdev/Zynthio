#!/usr/bin/env python3
import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class WorkerCorpusIngestor:
    def __init__(self, web_root="/var/www", corpus_dir="/root/zynthio/corpus"):
        self.web_root = Path(web_root)
        self.corpus_dir = Path(corpus_dir)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        self.metadata = []
        
        # Load worker config
        config_file = self.corpus_dir / "worker_config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {'worker_id': 0, 'site_range': [0, 806]}
        
    def scan_assigned_sites(self):
        sites = [d for d in self.web_root.iterdir() if d.is_dir() and not d.name.startswith('_')]
        start, end = self.config['site_range']
        return sites[start:end]
    
    def extract_content(self, site_path):
        content = []
        for html_file in site_path.rglob("*.html"):
            try:
                with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                    if len(text) > 100:
                        content.append({'file': str(html_file.relative_to(site_path)), 'text': text[:3000], 'site': site_path.name})
            except Exception as e:
                continue
        return content
    
    def build_corpus(self):
        sites = self.scan_assigned_sites()
        total_sites = len(sites)
        
        for i, site in enumerate(sites):
            print("Worker " + str(self.config['worker_id']) + " processing site " + str(i+1) + "/" + str(total_sites) + ": " + site.name)
            site_content = self.extract_content(site)
            for doc in site_content:
                self.documents.append(doc['text'])
                self.metadata.append({'site': doc['site'], 'file': doc['file'], 'url': "http://" + doc['site'] + "/" + doc['file'], 'worker': self.config['worker_id']})
        
        return len(sites)
    
    def create_index(self):
        print("Creating embeddings for " + str(len(self.documents)) + " documents...")
        embeddings = self.model.encode(self.documents, show_progress_bar=True)
        
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype('float32'))
        
        faiss.write_index(index, str(self.corpus_dir / "corpus.index"))
        
        with open(self.corpus_dir / "metadata.json", 'w') as f:
            json.dump(self.metadata, f)
        
        unique_sites = len(set(m['site'] for m in self.metadata))
        print("Worker " + str(self.config['worker_id']) + " indexed " + str(len(self.documents)) + " documents from " + str(unique_sites) + " sites")

if __name__ == "__main__":
    ingestor = WorkerCorpusIngestor()
    ingestor.build_corpus()
    ingestor.create_index()