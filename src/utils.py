#!/usr/bin/env python3
"""
Utility functions for UK Director Disqualification Scraper

This module contains helper functions used by the scraper.
"""

import os
import logging
import sys
from datetime import datetime
import pandas as pd
import re

def setup_logging(log_dir=None):
    """
    Set up logging configuration.
    
    Args:
        log_dir (str): Directory to store log files
    """
    # Create log directory if it doesn't exist
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    else:
        log_file = None
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file) if log_file else logging.NullHandler()
        ]
    )


def write_to_excel(df, output_path=None):
    """
    Write data to an Excel file with formatting.
    
    Args:
        df (pandas.DataFrame): DataFrame containing the scraped data
        output_path (str): Path to save the Excel file
        
    Returns:
        str: Path to the saved Excel file
    """
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"director_disqualification_data_{timestamp}.xlsx"
    
    # Create the Excel writer
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Disqualified Directors', index=False)
    
    # Get the workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['Disqualified Directors']
    
    # Add formatting
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#D9E1F2',
        'border': 1
    })
    
    # Apply the header format
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    
    # Set column widths
    worksheet.set_column('A:B', 20)  # Name and Company Name
    worksheet.set_column('C:F', 15)  # Date fields, etc.
    worksheet.set_column('G:G', 25)  # Address
    worksheet.set_column('H:H', 50)  # Conduct
    
    # Close the writer
    writer.close()
    
    return output_path


def extract_dates_from_text(text):
    """
    Extract dates from text in various formats.
    
    Args:
        text (str): Text containing dates
        
    Returns:
        list: List of extracted dates
    """
    # Common date formats in the UK
    patterns = [
        r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # DD/MM/YYYY or similar
        r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}'  # DD Month YYYY
    ]
    
    dates = []
    for pattern in patterns:
        dates.extend(re.findall(pattern, text, re.IGNORECASE))
    
    return dates


def extract_company_numbers(text):
    """
    Extract company registration numbers from text.
    
    Args:
        text (str): Text containing company numbers
        
    Returns:
        list: List of extracted company numbers
    """
    # UK company number pattern: typically 8 digits, sometimes with leading zeros
    pattern = r'\b\d{8}\b'
    return re.findall(pattern, text)
