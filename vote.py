#!/usr/bin/env python3
import sys
import time
from itertools import cycle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

def load_names(filename):
    """Load names from names.txt file sequentially"""
    names = []
    try:
        with open(filename, 'r') as f:
            names = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        sys.exit(1)
    return names

def load_proxies(filename):
    """Load proxies from proxies.txt file"""
    proxies = []
    try:
        with open(filename, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        sys.exit(1)
    
    if not proxies:
        print("Error: No proxies found in proxies.txt")
        sys.exit(1)
    
    return proxies

def create_driver(proxy):
    """Create a Selenium WebDriver with the specified proxy"""
    chrome_options = Options()
    
    # Configure proxy
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    
    # Additional options for better compatibility
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error creating WebDriver: {e}")
        return None

def submit_vote(driver, url, username):
    """Navigate to URL and submit vote with the given username"""
    try:
        driver.get(url)
        
        # Wait for the username field to be present
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        # Clear and fill the username field
        username_field.clear()
        username_field.send_keys(username)
        
        # Find and click the vote button
        # Adjust the selector based on your form's actual button
        vote_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"))
        )
        vote_button.click()
        
        print(f"Vote submitted for: {username}")
        time.sleep(2)  # Wait for submission to complete
        return True
        
    except Exception as e:
        print(f"Error submitting vote: {e}")
        return False
    finally:
        driver.quit()

def main():
    """Main function to orchestrate voting"""
    if len(sys.argv) != 2:
        print("Usage: python vote.py <URL>")
        print("Example: python vote.py https://example.com/voting-form")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)
    
    # Load names and proxies
    names = load_names('names.txt')
    proxies = load_proxies('proxies.txt')
    
    if not names:
        print("Error: No names found in names.txt")
        sys.exit(1)
    
    print(f"Loaded {len(names)} names from names.txt")
    print(f"Loaded {len(proxies)} proxies from proxies.txt")
    print(f"Target URL: {url}")
    print("-" * 50)
    
    # Create a rotating proxy cycle
    proxy_cycle = cycle(proxies)
    
    # Submit votes for each name with rotating proxies
    for i, name in enumerate(names, 1):
        proxy = next(proxy_cycle)
        print(f"[{i}/{len(names)}] Submitting vote for '{name}' using proxy: {proxy}")
        
        driver = create_driver(proxy)
        if driver:
            submit_vote(driver, url, name)
        else:
            print(f"Failed to create driver for vote #{i}")
        
        # Optional: Add delay between votes to avoid rate limiting
        if i < len(names):
            time.sleep(1)
    
    print("-" * 50)
    print("Voting complete!")

if __name__ == "__main__":
    main()
