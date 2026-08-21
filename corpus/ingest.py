#!/usr/bin/env python3
import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class SiteCorpusIngestor:
    def __init__(self, web_root="/var/www", corpus_dir="/root/zynthio/corpus"):
        self.web_root = Path(web_root)
        self.corpus_dir = Path(corpus_dir)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.documents = []
        self.metadata = []
    
    def scan_sites(self, limit=50):
        sites = [d for d in self.web_root.iterdir() if d.is_dir() and not d.name.startswith("_")]
        return sites[:limit]
    
    def extract_content(self, site_path):
        content = []
        for html_file in site_path.rglob("*.html"):
            try:
                with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                    if len(text) > 100:
                        content.append({"file": str(html_file.relative_to(site_path)), "text": text[:5000], "site": site_path.name})
            except Exception as e:
                continue
        return content
    
    def build_corpus(self, sites):
        for site in sites:
            print("Processing: " + site.name)
            site_content = self.extract_content(site)
            for doc in site_content:
                self.documents.append(doc["text"])
                self.metadata.append({"site": doc["site"], "file": doc["file"], "url": "http://" + doc["site"] + "/" + doc["file"]})
    
    def create_index(self):
        print("Creating embeddings...")
        embeddings = self.model.encode(self.documents, show_progress_bar=True)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype("float32"))
        faiss.write_index(index, str(self.corpus_dir / "corpus.index"))
        with open(self.corpus_dir / "metadata.json", "w") as f:
            json.dump(self.metadata, f)
        print("Indexed " + str(len(self.documents)) + " documents")
    
    def search(self, query, k=5):
        index = faiss.read_index(str(self.corpus_dir / "corpus.index"))
        with open(self.corpus_dir / "metadata.json", "r") as f:
            metadata = json.load(f)
        query_embedding = self.model.encode([query])
        distances, indices = index.search(query_embedding.astype("float32"), k)
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            results.append({"score": float(1 / (1 + dist)), "site": metadata[idx]["site"], "file": metadata[idx]["file"], "url": metadata[idx]["url"], "text": self.documents[idx][:500]})
        return results

if __name__ == "__main__":
    ingestor = SiteCorpusIngestor()
    sites = ingestor.scan_sites(limit=20)
    ingestor.build_corpus(sites)
    ingestor.create_index()
    results = ingestor.search("AI systems that work")
    print("Search Results:")
    for r in results:
        print(r["site"] + ": " + str(r["score"]) + " - " + r["file"])
