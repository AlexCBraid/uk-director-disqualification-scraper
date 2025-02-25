from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="uk-director-disqualification-scraper",
    version="0.1.0",
    author="Alex Braid",
    author_email="alex.c.braid@gmail.com",
    description="A tool to scrape UK company director disqualification data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/uk-director-disqualification-scraper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.6",
    install_requires=[
        "selenium>=4.10.0",
        "beautifulsoup4>=4.12.0",
        "pandas>=2.0.0",
        "xlsxwriter>=3.1.0",
        "webdriver-manager>=4.0.0",
        "python-dateutil>=2.8.2",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "director-scraper=src.scraper:scrape_data",
        ],
    },
)
