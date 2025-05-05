import arxiv
import pandas as pd
from datetime import datetime, timedelta
import logging
import os
from typing import List, Dict
import json
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('arxiv_fetcher.log'),
        logging.StreamHandler()
    ]
)

class ArxivFetcher:
    def __init__(self, config_path: str = 'config.json'):
        self.config = self._load_config(config_path)
        self.output_dir = self.config.get('output_dir', 'papers')
        os.makedirs(self.output_dir, exist_ok=True)
        self.fetched_papers_file = os.path.join(self.output_dir, 'fetched_papers.json')
        self.fetched_papers = self._load_fetched_papers()

    def _load_fetched_papers(self) -> set:
        """Load the set of previously fetched paper IDs."""
        try:
            if os.path.exists(self.fetched_papers_file):
                with open(self.fetched_papers_file, 'r') as f:
                    return set(json.load(f))
            return set()
        except Exception as e:
            logging.error(f"Error loading fetched papers: {str(e)}")
            return set()

    def _save_fetched_papers(self):
        """Save the set of fetched paper IDs to file."""
        try:
            with open(self.fetched_papers_file, 'w') as f:
                json.dump(list(self.fetched_papers), f)
        except Exception as e:
            logging.error(f"Error saving fetched papers: {str(e)}")

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Config file {config_path} not found")
            return {
                'categories': ['cs.CV'],
                'search_terms': ['image restoration'],
                'max_results': 20,
                'output_dir': 'papers'
            }

    def _analyze_abstract(self, abstract: str) -> Dict:
        """Analyze the abstract and extract key information."""
        # Split abstract into sentences
        sentences = re.split(r'(?<=[.!?])\s+', abstract)

        # Extract key points (first few sentences)
        key_points = sentences[:3]

        # Try to identify methodology
        methodology_keywords = ['propose', 'introduce', 'develop', 'present', 'method', 'approach', 'framework', 'network', 'model', 'algorithm']
        methodology = [s for s in sentences if any(kw in s.lower() for kw in methodology_keywords)]

        # Try to identify results
        results_keywords = ['achieve', 'improve', 'outperform', 'demonstrate', 'show', 'result', 'performance', 'accuracy', 'PSNR', 'SSIM']
        results = [s for s in sentences if any(kw in s.lower() for kw in results_keywords)]

        return {
            'key_points': key_points,
            'methodology': methodology[:2] if methodology else [],
            'results': results[:2] if results else []
        }

    def fetch_papers(self) -> List[Dict]:
        """Fetch papers from arXiv based on configured categories and search terms."""
        papers = []
        # 获取当前日期
        current_date = datetime.now()
        # 只获取最近7天的文章
        start_date = current_date - timedelta(days=7)

        for category in self.config['categories']:
            for search_term in self.config.get('search_terms', []):
                try:
                    query = f'cat:{category} AND {search_term}'
                    search = arxiv.Search(
                        query=query,
                        max_results=self.config.get('max_results', 20),
                        sort_by=arxiv.SortCriterion.SubmittedDate,
                        sort_order=arxiv.SortOrder.Descending
                    )

                    for result in search.results():
                        # 只处理最近7天的文章
                        if result.published.date() >= start_date.date():
                            # 检查是否已经获取过这篇文章
                            arxiv_id = result.entry_id.split('/')[-1]
                            if arxiv_id not in self.fetched_papers:
                                analysis = self._analyze_abstract(result.summary)
                                paper = {
                                    'title': result.title,
                                    'authors': [author.name for author in result.authors],
                                    'abstract': result.summary,
                                    'pdf_url': result.pdf_url,
                                    'published': result.published,
                                    'updated': result.updated,
                                    'category': category,
                                    'search_term': search_term,
                                    'arxiv_id': arxiv_id,
                                    'analysis': analysis
                                }
                                papers.append(paper)
                                # 记录已获取的文章ID
                                self.fetched_papers.add(arxiv_id)

                    logging.info(f"Successfully fetched papers for query: {query}")
                except Exception as e:
                    logging.error(f"Error fetching papers for query {query}: {str(e)}")

        # 保存已获取的文章ID
        self._save_fetched_papers()

        # 按发布日期降序排序
        papers.sort(key=lambda x: x['published'], reverse=True)
        return papers

    def _generate_markdown(self, paper: Dict) -> str:
        """Generate markdown summary for a paper."""
        analysis = paper['analysis']
        markdown = f"""# {paper['title']}

**Authors:** {', '.join(paper['authors'])}

**Category:** {paper['category']}

**Search Term:** {paper['search_term']}

**Published:** {paper['published'].strftime('%Y-%m-%d')}

## Key Points
{chr(10).join(f'- {point}' for point in analysis['key_points'])}

## Abstract
{paper['abstract']}

[PDF Link]({paper['pdf_url']})

---
"""
        return markdown

    def save_papers(self, papers: List[Dict]):
        """Save fetched papers to markdown file."""
        if not papers:
            logging.warning("No papers to save")
            return

        date_str = datetime.now().strftime('%Y-%m-%d')
        output_file = os.path.join(self.output_dir, f'papers_{date_str}.md')

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# arXiv Papers Summary - {date_str}\n\n")
                f.write(f"## Search Terms: {', '.join(self.config.get('search_terms', []))}\n\n")
                for paper in papers:
                    f.write(self._generate_markdown(paper))

            logging.info(f"Saved {len(papers)} papers to {output_file}")
        except Exception as e:
            logging.error(f"Error saving papers: {str(e)}")

def main():
    fetcher = ArxivFetcher()
    papers = fetcher.fetch_papers()
    fetcher.save_papers(papers)

if __name__ == "__main__":
    main()