from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from arxiv_fetcher import ArxivFetcher

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "categories": [],
            "search_terms": [],
            "max_results": 20,
            "output_dir": "papers"
        }

def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/update_config', methods=['POST'])
def update_config():
    config = {
        "categories": request.form.getlist('categories'),
        "search_terms": request.form.getlist('search_terms'),
        "max_results": int(request.form.get('max_results', 20)),
        "output_dir": request.form.get('output_dir', 'papers')
    }
    save_config(config)
    return redirect(url_for('index'))

@app.route('/fetch_papers', methods=['POST'])
def fetch_papers():
    try:
        fetcher = ArxivFetcher()
        fetcher.fetch_papers()
        return jsonify({"status": "success", "message": "Papers fetched successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)