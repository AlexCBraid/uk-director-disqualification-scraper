# Source Code Documentation

This directory contains the main source code for the UK Director Disqualification Scraper.

## File Structure

- `__init__.py`: Package initialization file
- `scraper.py`: Main entry point and scraping logic
- `parser.py`: HTML parsing and data extraction functions
- `utils.py`: Helper functions and utilities

## Module Overview

### scraper.py

The main module that handles:
- Setting up the Selenium WebDriver
- Navigating to the Insolvency Service database
- Finding and clicking on links to director details
- Coordinating the scraping process
- Saving the results to CSV files

Key functions:
- `setup_driver()`: Configure and initialize Chrome WebDriver
- `scrape_data()`: Main scraping function that orchestrates the process

### parser.py

This module handles parsing the HTML content from director detail pages:
- Extracting structured data from the raw HTML using BeautifulSoup
- Organizing the information into a standard dictionary format
- Cleaning and formatting the extracted data

Key functions:
- `parse_director_page(html_content)`: Parse HTML from a director detail page
- `clean_data(data_dict)`: Clean and format the extracted data

### utils.py

Contains various utility functions used throughout the scraper:
- Logging configuration
- Data export functions
- Text processing helpers

Key functions:
- `setup_logging(log_dir)`: Configure logging to file and console
- `write_to_excel(df, output_path)`: Export data to formatted Excel file
- `extract_dates_from_text(text)`: Helper for extracting dates from text
- `extract_company_numbers(text)`: Helper for extracting company numbers

## Usage

The main entry point is `scraper.py`. You can run it directly:

```bash
python -m src.scraper
```

Or import and use the functions in your own code:

```python
from src.scraper import scrape_data

# Run the scraper
data_df = scrape_data()

# Do something with the data
print(data_df.head())
```

## Configuration

Key configuration options in `scraper.py`:

- `CHROMEDRIVER_PATH`: Path to ChromeDriver executable
- `BASE_URL`: URL of the Insolvency Service database
- `TIMEOUT`: Maximum seconds to wait for page elements
- `WAIT_BETWEEN_REQUESTS`: Seconds to wait between requests (to avoid rate limiting)
- `MAX_RECORDS`: Maximum number of records to scrape
- `DATA_DIR`: Directory to save output files
- `LOG_DIR`: Directory to save log files

Update these variables to customize the scraper's behavior.
