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
                            'arxiv_id': result.entry_id.split('/')[-1],
                            'analysis': analysis
                        }
                        papers.append(paper)

                    logging.info(f"Successfully fetched papers for query: {query}")
                except Exception as e:
                    logging.error(f"Error fetching papers for query {query}: {str(e)}")

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

## Methodology
{chr(10).join(f'- {method}' for method in analysis['methodology'])}

## Results
{chr(10).join(f'- {result}' for result in analysis['results'])}

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