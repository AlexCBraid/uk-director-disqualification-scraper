#!/usr/bin/env python3
"""
Parser module for UK Director Disqualification Scraper

This module handles parsing the HTML content from the Insolvency Service
database pages and extracting structured data about disqualified directors.
"""

import logging
from bs4 import BeautifulSoup

# Setup logging
logger = logging.getLogger(__name__)

def parse_director_page(html_content):
    """
    Parse the HTML content of a director detail page.
    
    Args:
        html_content (str): HTML content of the page
        
    Returns:
        dict: Dictionary containing extracted director information
    """
    logger.debug("Parsing director detail page")
    
    # Create a dictionary to store the data
    data = {
        "Name": "",
        "Company Name": "",
        "Date of Birth": "",
        "Date Order Starts": "",
        "Disqualification Length": "",
        "CRO Number": "",
        "Last Known Address": "",
        "Conduct": ""
    }
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract name and company name
    try:
        name_tags = soup.find_all('b', string='Name:')
        if len(name_tags) > 0 and name_tags[0].next_sibling:
            data["Name"] = name_tags[0].next_sibling.strip()
        if len(name_tags) > 1 and name_tags[1].next_sibling:
            data["Company Name"] = name_tags[1].next_sibling.strip()
    except Exception as e:
        logger.error(f"Error parsing names: {e}")
    
    # Extract other fields
    fields_mapping = {
        "Date of Birth:": "Date of Birth",
        "Date Order Starts:": "Date Order Starts",
        "Disqualification Length:": "Disqualification Length",
        "CRO Number:": "CRO Number",
        "Last Known Address:": "Last Known Address"
    }
    
    for html_field, data_field in fields_mapping.items():
        try:
            field_tag = soup.find('b', string=html_field)
            if field_tag and field_tag.next_sibling:
                data[data_field] = field_tag.next_sibling.strip()
        except Exception as e:
            logger.error(f"Error parsing {data_field}: {e}")
    
    # Extract conduct (which has a different structure)
    try:
        conduct_tag = soup.find('b', string='Conduct:')
        if conduct_tag and conduct_tag.parent:
            data["Conduct"] = conduct_tag.parent.get_text(strip=True).replace('Conduct:', '').strip()
    except Exception as e:
        logger.error(f"Error parsing conduct: {e}")
    
    logger.debug(f"Parsed director data: {data['Name']}, {data['Company Name']}")
    return data


def clean_data(data_dict):
    """
    Clean and format the extracted data.
    
    Args:
        data_dict (dict): Raw extracted data
        
    Returns:
        dict: Cleaned and formatted data
    """
    # Create a copy to avoid modifying the original
    cleaned = data_dict.copy()
    
    # Clean address - remove excessive commas and whitespace
    if cleaned["Last Known Address"]:
        cleaned["Last Known Address"] = ", ".join(
            filter(None, [part.strip() for part in cleaned["Last Known Address"].split(',')])
        )
    
    # Format date fields if needed
    date_fields = ["Date of Birth", "Date Order Starts"]
    for field in date_fields:
        if cleaned[field]:
            # Remove any excessive whitespace
            cleaned[field] = " ".join(cleaned[field].split())
    
    return cleaned
