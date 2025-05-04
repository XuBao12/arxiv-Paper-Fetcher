# arXiv Paper Fetcher

A system that automatically fetches papers from arXiv for specific research fields.

## Features

- Automatically fetch papers from arXiv based on configured categories and search terms
- Web interface for easy configuration
- PDF download and organization
- Logging for tracking paper fetching activities
- Beautiful paper display interface with Markdown formatting
- Error handling and user-friendly error messages

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

2. Open your browser and navigate to `http://localhost:8080`

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

2. Access the web interface at `http://localhost:8080`

3. Configure your settings:
   - Select one or more arXiv categories
   - Add search terms (one per line)
   - Set the maximum number of results
   - Specify the output directory

4. Click "Fetch Papers Now" to:
   - Fetch papers from arXiv
   - Save them as Markdown files
   - Display them in a formatted view

### Command Line

To fetch papers manually:
```bash
python arxiv_fetcher.py
```

### Paper Display

After fetching papers, you'll see:
- Paper titles and authors
- Publication dates
- Key points from abstracts
- Full abstracts
- PDF download links

### Error Handling

The system provides clear error messages for:
- No papers found
- Network errors
- Configuration issues
- File system errors

## Directory Structure

```
arxiv-paper-fetcher/
├── app.py                 # Flask web application
├── arxiv_fetcher.py       # Main paper fetching logic
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── papers/                # Directory for downloaded papers
├── static/                # Static files for web interface
│   └── css/
│       └── style.css      # Custom styles
└── templates/             # HTML templates
    ├── index.html         # Main web interface
    ├── papers.html        # Paper display template
    ├── error.html         # Error page template
    └── no_papers.html     # No papers found template
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

## Troubleshooting

1. **No Papers Found**
   - Check your internet connection
   - Verify your search terms and categories
   - Ensure you have selected at least one category and search term

2. **API Rate Limits**
   - If you encounter rate limit errors, try:
     - Reducing the number of papers fetched
     - Adding delays between requests

3. **File System Errors**
   - Ensure the `papers` directory exists and is writable
   - Check file permissions
   - Verify disk space availability

## Contributing

Feel free to submit issues and enhancement requests!