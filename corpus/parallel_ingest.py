#!/usr/bin/env python3
import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from multiprocessing import Pool, cpu_count

class ParallelCorpusIngestor:
    def __init__(self, web_root="/var/www", corpus_dir="/root/zynthio/corpus"):
        self.web_root = Path(web_root)
        self.corpus_dir = Path(corpus_dir)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.num_workers = min(cpu_count(), 8)
        
    def scan_all_sites(self):
        sites = [d for d in self.web_root.iterdir() if d.is_dir() and not d.name.startswith('_')]
        return sites
    
    def extract_content_worker(self, site_data):
        site_path, site_index = site_data
        content = []
        try:
            for html_file in site_path.rglob("*.html"):
                try:
                    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                        if len(text) > 100:
                            content.append({
                                'file': str(html_file.relative_to(site_path)),
                                'text': text[:3000],
                                'site': site_path.name
                            })
                except Exception as e:
                    continue
        except Exception as e:
            pass
        
        return content
    
    def parallel_extract(self, sites):
        site_data = [(site, i) for i, site in enumerate(sites)]
        
        with Pool(self.num_workers) as pool:
            results = pool.map(self.extract_content_worker, site_data)
        
        all_content = []
        for result in results:
            all_content.extend(result)
        
        return all_content
    
    def create_index(self, documents, metadata):
        workers = self.num_workers
        print("Creating embeddings for " + str(len(documents)) + " documents using " + str(workers) + " workers...")
        embeddings = self.model.encode(documents, show_progress_bar=True, batch_size=32)
        
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype('float32'))
        
        faiss.write_index(index, str(self.corpus_dir / "corpus.index"))
        
        with open(self.corpus_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f)
        
        unique_sites = len(set(m['site'] for m in metadata))
        print("Indexed " + str(len(documents)) + " documents from " + str(unique_sites) + " sites")
        
    def process_all_sites(self):
        sites = self.scan_all_sites()
        total_sites = len(sites)
        workers = self.num_workers
        
        print("Starting parallel extraction of " + str(total_sites) + " sites using " + str(workers) + " workers")
        
        all_content = self.parallel_extract(sites)
        
        documents = [doc['text'] for doc in all_content]
        metadata = [{
            'site': doc['site'],
            'file': doc['file'],
            'url': "http://" + doc['site'] + "/" + doc['file']
        } for doc in all_content]
        
        self.create_index(documents, metadata)
        
        return len(documents), len(set(m['site'] for m in metadata))

if __name__ == "__main__":
    ingestor = ParallelCorpusIngestor()
    doc_count, site_count = ingestor.process_all_sites()
    print("Complete: " + str(doc_count) + " documents from " + str(site_count) + " sites")