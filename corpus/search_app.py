#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import faiss

app = Flask(__name__)
CORS(app)

print('Loading model...')
model = SentenceTransformer('all-MiniLM-L6-v2')
print('Loading index...')
index = faiss.read_index('corpus_FINAL_20260820.index')
print(f'Loaded {index.ntotal} documents')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>VDS Corpus Search</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .search-box { margin: 20px 0; }
        input[type="text"] { width: 70%; padding: 10px; font-size: 16px; }
        button { padding: 10px 20px; font-size: 16px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .results { margin-top: 20px; }
        .result { padding: 10px; margin: 10px 0; border-left: 3px solid #007bff; background: #f8f9fa; }
        .score { color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <h1>VDS Corpus Search</h1>
    <p>Search across 5116 documents from 2708+ domains</p>
    
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
                const response = await fetch('/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                
                if (data.results && data.results.length > 0) {
                    let html = '<h2>Results</h2>';
                    data.results.forEach((result, i) => {
                        html += '<div class="result">';
                        html += '<strong>Result ' + (i + 1) + '</strong><br>';
                        html += '<span class="score">Score: ' + result.score.toFixed(4) + '</span><br>';
                        html += '<span class="score">Document ID: ' + result.doc_id + '</span>';
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
    return render_template_string(HTML_TEMPLATE)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k=5)
    
    results = []
    for i, (doc_id, distance) in enumerate(zip(indices[0], distances[0])):
        results.append({
            'doc_id': int(doc_id),
            'score': float(distance)
        })
    
    return jsonify({
        'query': query,
        'results': results,
        'total': len(results)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
