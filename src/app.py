from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from src.arxiv_fetcher import ArxivFetcher
import markdown
from datetime import datetime

app = Flask(__name__,
           template_folder='templates',
           static_folder='static')
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
        # 确保 papers 目录存在
        os.makedirs('papers', exist_ok=True)

        fetcher = ArxivFetcher()
        papers = fetcher.fetch_papers()

        # 保存论文到文件
        fetcher.save_papers(papers)

        # 生成当前日期的文件名
        current_date = datetime.now().strftime('%Y-%m-%d')
        output_file = os.path.join('papers', f'papers_{current_date}.md')

        # 检查文件是否已经存在
        if not os.path.exists(output_file):
            return jsonify({
                "status": "error",
                "message": "No papers were fetched. Please check your configuration and try again."
            }), 404

        # 读取生成的 Markdown 文件内容
        with open(output_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # 将 Markdown 转换为 HTML
        html_content = markdown.markdown(markdown_content, extensions=['fenced_code', 'tables'])

        return jsonify({
            "status": "success",
            "message": "Papers fetched successfully",
            "content": html_content
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/papers/<date>')
def show_papers(date):
    try:
        output_file = os.path.join('papers', f'papers_{date}.md')
        if not os.path.exists(output_file):
            return render_template('no_papers.html', date=date)

        with open(output_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        html_content = markdown.markdown(markdown_content, extensions=['fenced_code', 'tables'])
        return render_template('papers.html', content=html_content, date=date)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)