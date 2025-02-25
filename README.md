UK Director Disqualification Scraper
A Python tool that automatically collects information about recently disqualified UK company directors from the Insolvency Service database.
📋 Overview
This tool scrapes the UK Insolvency Service database to collect information about recently disqualified company directors and saves the data to a CSV file. It provides a more accessible way to monitor director disqualifications than the official search methods, which require specific information about directors.
Key features:

Automatically collects all recent disqualification data
Creates a persistent record of director disqualifications (which are only displayed for 3 months on the official site)
Extracts detailed misconduct information
Enables analysis of disqualification trends and patterns

🔍 Why This Tool Exists
In the UK, company directors who fail to meet their legal responsibilities can be disqualified for up to 15 years. While this information is public, there are limitations in how it can be accessed:

The Insolvency Service only displays recent disqualifications for 3 months
The Companies House search requires specific director details
There's no simple way to download the data in bulk for analysis

This tool addresses these limitations by providing a simple way to collect and save all disqualification data.
📊 Data Collected
For each disqualified director, the scraper collects:

Name of the disqualified individual
Company name
Date of birth (when available)
Start date of disqualification
Disqualification length (years and months)
Company Registration Office (CRO) number
Last known address
Detailed description of misconduct/unfit conduct

🚀 Getting Started
Prerequisites

Python 3.6 or higher
Chrome browser installed
ChromeDriver (must be compatible with your Chrome version)

Installation
bashCopy# Clone the repository
git clone https://github.com/yourusername/uk-director-disqualification-scraper.git
cd uk-director-disqualification-scraper

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Configuration
Before running the scraper, update the ChromeDriver path in src/scraper.py:
pythonCopy# Update this to your ChromeDriver path
CHROMEDRIVER_PATH = "/path/to/your/chromedriver"
You can also adjust other settings like:

MAX_RECORDS: Number of records to scrape (default: 200)
WAIT_BETWEEN_REQUESTS: Seconds to wait between requests (default: 2)
TIMEOUT: Maximum seconds to wait for page elements (default: 10)

Running the Scraper
bashCopy# Run from the project root directory
python -m src.scraper
The results will be saved to data/director_disqualification_data.csv.
📈 Sample Output
The CSV output contains the following columns:
CopyName, Company Name, Date of Birth, Date Order Starts, Disqualification Length, CRO Number, Last Known Address, Conduct
Example entry:
CopyMagdalena Bejma, MORBUS LIMITED, /  /, 19/2/2025, 9 years Years 0 Month(s), 9403055, Flat 2 4 Shaftesbury Avenue LEEDS LS8 1DT, "Magdalena Bejma made false representations in an application for a Bounce Back Loan..."
⚖️ Legal and Ethical Considerations

This tool only accesses publicly available information
The scraping is done at a reasonable rate to avoid overloading the source website
The collected information should be used in accordance with data protection regulations

🛠️ Technical Details
The scraper uses:

Selenium WebDriver for browser automation
BeautifulSoup for HTML parsing
Pandas for data manipulation and CSV export

For more details, see the code documentation.
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
