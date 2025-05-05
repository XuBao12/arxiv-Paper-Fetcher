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

# GitHub仓库URL
GITHUB_REPO_URL = "https://github.com/XuBao12/arxiv-Paper-Fetcher"

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
    return render_template('index.html', config=config, github_url=GITHUB_REPO_URL)

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
        # 加载配置
        config = load_config()
        output_dir = config.get('output_dir', 'papers')

        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        fetcher = ArxivFetcher()
        papers = fetcher.fetch_papers()

        # 保存论文到文件
        fetcher.save_papers(papers)

        # 生成当前日期的文件名
        current_date = datetime.now().strftime('%Y-%m-%d')
        output_file = os.path.join(output_dir, f'papers_{current_date}.md')

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
        # 加载配置
        config = load_config()
        output_dir = config.get('output_dir', 'papers')

        output_file = os.path.join(output_dir, f'papers_{date}.md')
        if not os.path.exists(output_file):
            return render_template('no_papers.html', date=date, github_url=GITHUB_REPO_URL)

        with open(output_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        html_content = markdown.markdown(markdown_content, extensions=['fenced_code', 'tables'])
        return render_template('papers.html', content=html_content, date=date, github_url=GITHUB_REPO_URL)
    except Exception as e:
        return render_template('error.html', error=str(e), github_url=GITHUB_REPO_URL)

@app.route('/browse_directory', methods=['POST'])
def browse_directory():
    try:
        # 获取要浏览的目录路径
        current_path = request.json.get('path', os.path.expanduser('~'))

        # 如果路径为空，使用用户主目录
        if not current_path:
            current_path = os.path.expanduser('~')

        # 安全检查，确保路径在允许的范围内
        if not current_path.startswith(os.path.expanduser('~')):
            current_path = os.path.expanduser('~')

        # 检查路径是否存在
        if not os.path.exists(current_path):
            return jsonify({'status': 'error', 'message': 'Path does not exist'}), 404

        # 获取目录内容
        items = []
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                items.append({
                    'name': item,
                    'path': item_path,
                    'type': 'directory'
                })

        # 获取父目录
        parent_path = os.path.dirname(current_path)
        if parent_path.startswith(os.path.expanduser('~')):
            parent = {'path': parent_path}
        else:
            parent = None

        return jsonify({
            'status': 'success',
            'path': current_path,
            'items': items,
            'parent': parent
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/create_directory', methods=['POST'])
def create_directory():
    try:
        parent = request.json.get('parent', os.path.expanduser('~'))
        name = request.json.get('name', '')

        # 安全检查
        if not parent.startswith(os.path.expanduser('~')):
            return jsonify({'status': 'error', 'message': 'Invalid parent path'}), 400

        # 创建目录
        new_dir = os.path.join(parent, name)
        os.makedirs(new_dir, exist_ok=True)

        return jsonify({
            'status': 'success',
            'path': new_dir
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)