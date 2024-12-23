"""
Etherscan Address Scraper
-------------------------
A Python script to scrape Ethereum addresses from Etherscan's top accounts pages. (https://etherscan.io/accounts/1)

Features:
- Scrapes TOP addresses from pages 1-400 on etherscan.io/accounts
- Saves unique addresses to a YAML file in list format
- Includes progress tracking and error handling
- Implements rate limiting to avoid IP blocks

Usage:
    python scrape_addresses.py
"""

import requests
from bs4 import BeautifulSoup
import time
import re
import yaml

# Global variables, start and end page
START_PAGE = 1
END_PAGE = 400

def get_addresses_from_page(page_num):
    url = f"https://etherscan.io/accounts/{page_num}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    try:
        time.sleep(1)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all spans with data-highlight-target attribute
        address_spans = soup.find_all('span', attrs={'data-highlight-target': True})
        
        # Extract addresses
        addresses = []
        for span in address_spans:
            address = span['data-highlight-target']
            if address.startswith('0x') and len(address) == 42:  # Ensure it's a valid ETH address
                addresses.append(address)
        
        return list(set(addresses))
        
    except Exception as e:
        print(f"Error scraping page {page_num}: {str(e)}")
        return []

def save_addresses(addresses, filename='data/scraped-addresses.yaml'):
    # Convert addresses set to sorted list
    addresses_list = sorted(list(addresses))
    
    # Save as YAML
    with open(filename, 'w') as f:
        yaml.dump(addresses_list, f, default_flow_style=False)

def main():
    all_addresses = set()
    
    print("Starting to scrape addresses...")
    
    for page in range(START_PAGE, END_PAGE + 1):
        print(f"Scraping page {page}/{END_PAGE}...")
        page_addresses = get_addresses_from_page(page)
        
        if page_addresses:
            all_addresses.update(page_addresses)
            print(f"Found {len(page_addresses)} addresses on page {page}")
        else:
            print(f"No addresses found on page {page}, retrying...")
            time.sleep(5)  # Wait longer before retry
            page_addresses = get_addresses_from_page(page)
            if page_addresses:
                all_addresses.update(page_addresses)
                print(f"Retry successful: Found {len(page_addresses)} addresses on page {page}")
        
        # Save progress every 10 pages
        if page % 10 == 0:
            save_addresses(all_addresses)
            print(f"Progress saved: {len(all_addresses)} unique addresses found so far")
        
        # Random delay between pages
        time.sleep(2)
    
    # Final save
    save_addresses(all_addresses)
    print(f"Scraping complete! Total unique addresses found: {len(all_addresses)}")

if __name__ == "__main__":
    main()