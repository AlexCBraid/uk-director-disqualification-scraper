#!/usr/bin/env python3
"""
UK Director Disqualification Scraper

This module contains the main functionality for scraping information about
disqualified directors from the UK Insolvency Service database.
"""

import time
import os
import logging
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from parser import parse_director_page
from utils import setup_logging

# Setup logging
logger = logging.getLogger(__name__)

# Configuration (update these as needed)
CHROMEDRIVER_PATH = "/Users/braidosan/chromedriver_new/chromedriver-mac-x64/chromedriver"
BASE_URL = 'https://www.insolvencydirect.bis.gov.uk/IESdatabase/viewdirectorsummary-new.asp'
TIMEOUT = 10
MAX_RETRIES = 3
WAIT_BETWEEN_REQUESTS = 2
MAX_RECORDS = 200  # Adjust as needed
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')


def setup_driver():
    """
    Set up and configure the Chrome WebDriver.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance
    """
    logger.info("Setting up Chrome WebDriver...")
    options = Options()
    
    # Comment this line if you want to see the browser
    # options.add_argument("--headless")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Create the service with our downloaded driver
    service = Service(executable_path=CHROMEDRIVER_PATH)
    
    # Create and return the driver
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def scrape_data():
    """
    Main function to scrape disqualified director data.
    
    Returns:
        pandas.DataFrame: DataFrame containing the scraped data
    """
    setup_logging(LOG_DIR)
    logger.info("Starting the scraper...")
    
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    driver = setup_driver()
    
    try:
        # Navigate to the main page
        logger.info(f"Navigating to {BASE_URL}")
        driver.get(BASE_URL)
        
        # Wait for the page to load
        logger.info("Waiting for page to load...")
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Click here to view')]"))
        )
        
        # Get all the detail links
        logger.info("Finding detail links...")
        details_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Click here to view')]")
        num_records = min(MAX_RECORDS, len(details_links))
        logger.info(f"Found {len(details_links)} records. Will scrape {num_records} records.")
        
        # Prepare to store the data
        all_data = []
        
        # Loop through the records
        for i in range(num_records):
            logger.info(f"Processing record {i+1}/{num_records}")
            
            # Click on the detail link
            details_links[i].click()
            
            # Wait for the detail page to load
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Parse the page using our parser module
            data = parse_director_page(driver.page_source)
            
            # Add the data to our list
            all_data.append(data)
            
            # Go back to the main page
            driver.back()
            
            # Wait for the main page to reload
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Click here to view')]"))
            )
            
            # Refresh the details_links
            details_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Click here to view')]"))
            
            # Wait between requests to be polite
            time.sleep(WAIT_BETWEEN_REQUESTS)
        
        # Create a DataFrame
        df = pd.DataFrame(all_data)
        logger.info(f"Successfully scraped {len(df)} records")
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = os.path.join(DATA_DIR, f"director_disqualification_data_{timestamp}.csv")
        df.to_csv(csv_filename, index=False)
        logger.info(f"Data saved to {csv_filename}")
        
        return df
    
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise
    
    finally:
        # Close the browser
        logger.info("Closing browser...")
        driver.quit()


if __name__ == "__main__":
    # Execute the scraper when run directly
    scrape_data()
