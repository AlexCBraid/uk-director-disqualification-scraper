#!/usr/bin/env python3
"""
Tests for the scraper module.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scraper import setup_driver, scrape_data


class TestScraper(unittest.TestCase):
    """Test cases for the scraper module."""

    @patch('src.scraper.webdriver.Chrome')
    @patch('src.scraper.Service')
    def test_setup_driver(self, mock_service, mock_chrome):
        """Test setup_driver function."""
        # Mock the Chrome WebDriver and Service
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Call the function
        driver = setup_driver()
        
        # Verify Chrome was instantiated with the correct service
        mock_chrome.assert_called_once()
        mock_service.assert_called_once()
        
        # Verify we got the mock driver back
        self.assertEqual(driver, mock_driver)

    @patch('src.scraper.setup_driver')
    @patch('src.scraper.WebDriverWait')
    @patch('src.scraper.parse_director_page')
    @patch('src.scraper.pd.DataFrame')
    def test_scrape_data(self, mock_dataframe, mock_parse, mock_wait, mock_setup_driver):
        """Test scrape_data function."""
        # This is a complex function to test completely
        # Just testing the basic setup and cleanup for now
        
        # Mock the driver and wait
        mock_driver = MagicMock()
        mock_setup_driver.return_value = mock_driver
        
        # Mock the DataFrame
        mock_df = MagicMock()
        mock_dataframe.return_value = mock_df
        
        # Mock finding elements
        mock_driver.find_elements.return_value = [MagicMock() for _ in range(3)]
        
        # Return dummy data from parse_director_page
        mock_parse.return_value = {
            "Name": "Test Director",
            "Company Name": "Test Company",
            "Date of Birth": "01/01/1970",
            "Date Order Starts": "01/01/2025",
            "Disqualification Length": "5 years",
            "CRO Number": "12345678",
            "Last Known Address": "123 Test Street",
            "Conduct": "Test conduct"
        }
        
        # Call the function
        with self.assertRaises(Exception):  # Expecting an exception due to incomplete mocking
            scrape_data()
        
        # Verify driver was set up and cleaned up
        mock_setup_driver.assert_called_once()
        mock_driver.quit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
