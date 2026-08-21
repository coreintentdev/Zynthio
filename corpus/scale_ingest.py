#!/usr/bin/env python3
import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class ScalableCorpusIngestor:
    def __init__(self, web_root="/var/www", corpus_dir="/root/zynthio/corpus"):
        self.web_root = Path(web_root)
        self.corpus_dir = Path(corpus_dir)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        self.metadata = []
        
    def scan_all_sites(self):
        sites = [d for d in self.web_root.iterdir() if d.is_dir() and not d.name.startswith('_')]
        return sites
    
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
    
    def incremental_build(self, start_index=0, batch_size=100):
        sites = self.scan_all_sites()
        total_sites = len(sites)
        
        for i in range(start_index, min(start_index + batch_size, total_sites)):
            site = sites[i]
            print("Processing site " + str(i+1) + "/" + str(total_sites) + ": " + site.name)
            site_content = self.extract_content(site)
            for doc in site_content:
                self.documents.append(doc['text'])
                self.metadata.append({'site': doc['site'], 'file': doc['file'], 'url': "http://" + doc['site'] + "/" + doc['file']})
        
        return i + 1
    
    def append_to_index(self):
        try:
            index = faiss.read_index(str(self.corpus_dir / "corpus.index"))
            with open(self.corpus_dir / "metadata.json", 'r') as f:
                existing_metadata = json.load(f)
        except:
            index = None
            existing_metadata = []
        
        print("Creating embeddings for " + str(len(self.documents)) + " new documents...")
        embeddings = self.model.encode(self.documents, show_progress_bar=True)
        
        if index is None:
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings.astype('float32'))
        else:
            index.add(embeddings.astype('float32'))
        
        faiss.write_index(index, str(self.corpus_dir / "corpus.index"))
        
        all_metadata = existing_metadata + self.metadata
        with open(self.corpus_dir / "metadata.json", 'w') as f:
            json.dump(all_metadata, f)
        
        print("Total indexed: " + str(len(all_metadata)) + " documents (+" + str(len(self.metadata)) + " new)")
        
    def search(self, query, k=5):
        index = faiss.read_index(str(self.corpus_dir / "corpus.index"))
        with open(self.corpus_dir / "metadata.json", 'r') as f:
            metadata = json.load(f)
        
        query_embedding = self.model.encode([query])
        distances, indices = index.search(query_embedding.astype('float32'), k)
        
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            results.append({'score': float(1 / (1 + dist)), 'site': metadata[idx]['site'], 'file': metadata[idx]['file'], 'url': metadata[idx]['url']})
        
        return results

if __name__ == "__main__":
    ingestor = ScalableCorpusIngestor()
    
    progress_file = ingestor.corpus_dir / "progress.json"
    if progress_file.exists():
        with open(progress_file, 'r') as f:
            progress = json.load(f)
        start_index = progress.get('last_index', 0)
    else:
        start_index = 0
    
    next_index = ingestor.incremental_build(start_index, batch_size=50)
    
    with open(progress_file, 'w') as f:
        json.dump({'last_index': next_index}, f)
    
    ingestor.append_to_index()
    
    results = ingestor.search("AI systems that work")
    print("Search Results:")
    for r in results:
        print(r['site'] + ": " + str(r['score']) + " - " + r['file'])