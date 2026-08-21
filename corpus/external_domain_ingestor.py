#!/usr/bin/env python3
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import requests
from bs4 import BeautifulSoup
import time
import sys

class ExternalDomainIngestor:
    def __init__(self, corpus_dir="/root/zynthio/corpus"):
        self.corpus_dir = Path(corpus_dir)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def load_existing_corpus(self):
        try:
            index = faiss.read_index(str(self.corpus_dir / "corpus.index"))
            with open(self.corpus_dir / "metadata.json", 'r') as f:
                metadata = json.load(f)
            return index, metadata
        except:
            return None, []
    
    def scrape_domain(self, domain):
        url = "http://" + domain if not domain.startswith('http') else domain
        content = []
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text(separator=' ', strip=True)
                if len(text) > 100:
                    content.append({
                        'domain': domain,
                        'url': url,
                        'text': text[:5000],
                        'title': soup.title.string if soup.title else domain
                    })
        except Exception as e:
            print("Error scraping " + domain + ": " + str(e))
        
        return content
    
    def ingest_domains(self, domains, batch_size=50):
        all_content = []
        
        for i, domain in enumerate(domains):
            print("Processing external domain " + str(i+1) + "/" + str(len(domains)) + ": " + domain)
            domain_content = self.scrape_domain(domain)
            all_content.extend(domain_content)
            
            if len(all_content) >= batch_size:
                self.add_to_corpus(all_content)
                all_content = []
        
        if all_content:
            self.add_to_corpus(all_content)
    
    def add_to_corpus(self, new_content):
        index, existing_metadata = self.load_existing_corpus()
        
        new_documents = [doc['text'] for doc in new_content]
        new_metadata = [{
            'domain': doc['domain'],
            'url': doc['url'],
            'title': doc['title'],
            'source': 'external'
        } for doc in new_content]
        
        print("Creating embeddings for " + str(len(new_documents)) + " new documents...")
        embeddings = self.model.encode(new_documents, show_progress_bar=True)
        
        if index is None:
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            all_metadata = new_metadata
        else:
            index.add(embeddings.astype('float32'))
            all_metadata = existing_metadata + new_metadata
        
        faiss.write_index(index, str(self.corpus_dir / "corpus.index"))
        
        with open(self.corpus_dir / "metadata.json", 'w') as f:
            json.dump(all_metadata, f)
        
        print("Total corpus: " + str(len(all_metadata)) + " documents")
        
    def load_domains_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                domains = [line.strip() for line in f if line.strip()]
            return domains
        except Exception as e:
            print("Error loading domains: " + str(e))
            return []

def main():
    if len(sys.argv) < 2:
        print("External Domain Ingestor")
        print("Usage: python external_domain_ingestor.py <domains_file.txt>")
        print("File format: one domain per line")
        return
    
    domains_file = sys.argv[1]
    ingestor = ExternalDomainIngestor()
    
    domains = ingestor.load_domains_from_file(domains_file)
    print("Loaded " + str(len(domains)) + " domains from " + domains_file)
    
    ingestor.ingest_domains(domains, batch_size=100)
    
    print("External domain ingestion complete")

if __name__ == "__main__":
    main()