# arXiv Paper Fetcher

A system that automatically fetches papers from arXiv for specific research fields.

## Features

- Automatically fetch papers from arXiv based on configured categories and search terms
- Daily automatic updates via cron job
- Web interface for easy configuration
- PDF download and organization
- Logging for tracking paper fetching activities

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/arxiv-paper-fetcher.git
cd arxiv-paper-fetcher
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Web Interface

1. Start the web server:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Configure your settings:
   - Select arXiv categories (e.g., cs.CV for Computer Vision)
   - Add search terms
   - Set maximum number of results
   - Specify output directory

4. Click "Save Configuration" to save your settings

5. Click "Fetch Papers Now" to manually trigger paper fetching

### Manual Configuration

You can also manually edit the `config.json` file:

```json
{
    "categories": [
        "cs.CV"
    ],
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

### Web Interface

1. Start the web server:
```bash
python app.py
```

2. Access the web interface at `http://localhost:5000`

3. Configure your settings and fetch papers

### Command Line

To fetch papers manually:
```bash
python run_daily.py
```

### Automatic Updates

To set up automatic daily updates:

1. Open your crontab:
```bash
crontab -e
```

2. Add the following line to run the script daily at 8:00 AM:
```bash
0 8 * * * cd /path/to/arxiv-paper-fetcher && python run_daily.py >> arxiv_fetcher.log 2>&1
```

## Directory Structure

```
arxiv-paper-fetcher/
├── app.py                 # Flask web application
├── arxiv_fetcher.py       # Main paper fetching logic
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── run_daily.py           # Script for daily execution
├── papers/                # Directory for downloaded papers
├── static/                # Static files for web interface
│   └── css/
│       └── style.css      # Custom styles
└── templates/             # HTML templates
    └── index.html         # Main web interface
```

## Logging

The system logs all activities to `arxiv_fetcher.log`. You can check this file to monitor the paper fetching process and troubleshoot any issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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