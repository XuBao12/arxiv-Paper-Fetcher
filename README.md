# arXiv Paper Fetcher

This system automatically fetches papers from arXiv for specified research categories on a daily basis.

## Features

- **Automated Paper Fetching**: Daily retrieval of papers from specified arXiv categories
- **Smart Analysis**: Automatic extraction of key points, methodology, and results
- **Customizable Search**: Support for multiple search terms and categories
- **Structured Output**: Generate detailed Markdown reports with paper summaries

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the categories and search terms in `config.json`:
- Edit the `categories` list to include the arXiv categories you're interested in
- Add `search_terms` to specify keywords for paper search
- Adjust `max_results` to control how many papers to fetch per category
- Change `output_dir` to specify where to save the papers

Example configuration for image restoration papers:
```json
{
    "categories": ["cs.CV"],
    "search_terms": [
        "image restoration",
        "image reconstruction",
        "image denoising",
        "image super-resolution",
        "image inpainting"
    ],
    "max_results": 20,
    "output_dir": "papers"
}
```

## Usage

### Basic Usage
To fetch papers immediately:
```bash
python arxiv_fetcher.py
```

### Daily Automatic Run
To start the daily fetcher:
```bash
python run_daily.py
```

The script will run every day at 8:00 AM and save the results in the specified output directory.

## Output

Papers are saved in Markdown format with the following sections:
- Title and Authors
- Category and Search Terms
- Publication Date
- Key Points (automatically extracted)
- Methodology (automatically extracted)
- Results (automatically extracted)
- Full Abstract
- PDF Link

Files are named with the date format: `papers_YYYY-MM-DD.md`

## Logging

Logs are saved in `arxiv_fetcher.log` and also displayed in the console.

## Available arXiv Categories

Some common categories:
- cs.AI (Artificial Intelligence)
- cs.CL (Computation and Language)
- cs.LG (Machine Learning)
- cs.CV (Computer Vision)
- cs.NE (Neural and Evolutionary Computing)
- stat.ML (Machine Learning)

For a complete list of categories, visit: https://arxiv.org/help/api/user-manual#subject_classifications

## Cost and Limitations

- **arXiv API**: Free to use, with rate limits (recommended: no more than 1 request per minute)
- **Storage**: Local storage only, no cloud costs
- **Network**: Only requires standard internet connection

## Troubleshooting

1. **API Rate Limits**: If you encounter rate limit errors, try:
   - Reducing the number of papers fetched
   - Adding delays between requests
   - Using the daily scheduler instead of frequent manual runs

## Contributing

Feel free to submit issues and enhancement requests!