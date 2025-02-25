#!/usr/bin/env python3
"""
Tests for the parser module.
"""

import unittest
import os
import sys

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import parse_director_page, clean_data


class TestParser(unittest.TestCase):
    """Test cases for the parser module."""

    def test_parse_director_page(self):
        """Test parse_director_page function with a sample HTML."""
        # Sample HTML similar to what we'd get from the Insolvency Service
        sample_html = """
        <html>
            <body>
                <b>Name:</b> John Smith
                <br>
                <b>Name:</b> TEST COMPANY LTD
                <br>
                <b>Date of Birth:</b> 01/01/1970
                <br>
                <b>Date Order Starts:</b> 15/02/2025
                <br>
                <b>Disqualification Length:</b> 5 Years 0 Month(s)
                <br>
                <b>CRO Number:</b> 12345678
                <br>
                <b>Last Known Address:</b> 123 Test Street, Test City, TS1 2AB
                <br>
                <b>Conduct:</b> John Smith failed to maintain adequate accounting records...
            </body>
        </html>
        """
        
        # Parse the HTML
        result = parse_director_page(sample_html)
        
        # Check the results
        self.assertEqual(result["Name"], "John Smith")
        self.assertEqual(result["Company Name"], "TEST COMPANY LTD")
        self.assertEqual(result["Date of Birth"], "01/01/1970")
        self.assertEqual(result["Date Order Starts"], "15/02/2025")
        self.assertEqual(result["Disqualification Length"], "5 Years 0 Month(s)")
        self.assertEqual(result["CRO Number"], "12345678")
        self.assertEqual(result["Last Known Address"], "123 Test Street, Test City, TS1 2AB")
        self.assertTrue(result["Conduct"].startswith("John Smith failed"))

    def test_clean_data(self):
        """Test clean_data function."""
        # Sample raw data
        raw_data = {
            "Name": "John  Smith",
            "Company Name": "TEST COMPANY LTD",
            "Date of Birth": "01 / 01 / 1970",
            "Date Order Starts": "15 / 02 / 2025",
            "Disqualification Length": "5 Years 0 Month(s)",
            "CRO Number": "12345678",
            "Last Known Address": "123 Test Street, , Test City, , TS1 2AB",
            "Conduct": "John Smith failed to maintain adequate accounting records..."
        }
        
        # Clean the data
        cleaned = clean_data(raw_data)
        
        # Check the results
        self.assertEqual(cleaned["Name"], "John  Smith")  # Name shouldn't change
        self.assertEqual(cleaned["Date of Birth"], "01 / 01 / 1970")  # Dates are preserved but excess space removed
        self.assertEqual(cleaned["Last Known Address"], "123 Test Street, Test City, TS1 2AB")  # Excess commas removed


if __name__ == '__main__':
    unittest.main()
