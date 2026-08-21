#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import faiss
import json

app = Flask(__name__)
CORS(app)

print('Loading model...')
model = SentenceTransformer('all-MiniLM-L6-v2')
print('Loading index...')
index = faiss.read_index('corpus_FINAL_20260820.index')
print(f'Loaded {index.ntotal} documents')

# Load metadata
try:
    with open('metadata_FINAL_20260820.json', 'r') as f:
        metadata = json.load(f)
    print(f'Loaded {len(metadata)} metadata entries')
except:
    metadata = {}
    print('No metadata file found')

RAG_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>VDS Enhanced RAG Search</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .search-box { margin: 20px 0; }
        input[type="text"] { width: 70%; padding: 10px; font-size: 16px; }
        button { padding: 10px 20px; font-size: 16px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .results { margin-top: 20px; }
        .result { padding: 15px; margin: 10px 0; border-left: 3px solid #007bff; background: #f8f9fa; }
        .score { color: #666; font-size: 14px; }
        .metadata { color: #888; font-size: 12px; margin-top: 5px; }
        .context { background: #e9ecef; padding: 10px; margin-top: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>VDS Enhanced RAG Search</h1>
    <p>Advanced retrieval-augmented generation across 5116 documents</p>
    
    <div class="search-box">
        <input type="text" id="query" placeholder="Enter your search query..." />
        <button onclick="search()">Search</button>
    </div>
    
    <div id="results" class="results"></div>
    
    <script>
        async function search() {
            const query = document.getElementById('query').value;
            const resultsDiv = document.getElementById('results');
            
            if (!query) {
                resultsDiv.innerHTML = '<p>Please enter a search query.</p>';
                return;
            }
            
            resultsDiv.innerHTML = '<p>Searching...</p>';
            
            try {
                const response = await fetch('/rag_search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query, k: 5 })
                });
                
                const data = await response.json();
                
                if (data.results && data.results.length > 0) {
                    let html = '<h2>Results</h2>';
                    data.results.forEach((result, i) => {
                        html += '<div class="result">';
                        html += '<strong>Result ' + (i + 1) + '</strong><br>';
                        html += '<span class="score">Score: ' + result.score.toFixed(4) + '</span><br>';
                        html += '<span class="metadata">Document ID: ' + result.doc_id + '</span>';
                        if (result.source) {
                            html += '<span class="metadata">Source: ' + result.source + '</span>';
                        }
                        html += '</div>';
                    });
                    resultsDiv.innerHTML = html;
                } else {
                    resultsDiv.innerHTML = '<p>No results found.</p>';
                }
            } catch (error) {
                resultsDiv.innerHTML = '<p>Error: ' + error + '</p>';
            }
        }
        
        document.getElementById('query').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') search();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(RAG_TEMPLATE)

@app.route('/rag_search', methods=['POST'])
def rag_search():
    data = request.json
    query = data.get('query', '')
    k = data.get('k', 5)
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k=k)
    
    results = []
    for doc_id, distance in zip(indices[0], distances[0]):
        result = {
            'doc_id': int(doc_id),
            'score': float(distance)
        }
        
        # Add metadata if available
        if metadata and str(doc_id) in metadata:
            result['source'] = metadata[str(doc_id)].get('source', 'unknown')
            result['url'] = metadata[str(doc_id)].get('url', '')
        
        results.append(result)
    
    return jsonify({
        'query': query,
        'results': results,
        'total': len(results),
        'corpus_size': index.ntotal
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False)
