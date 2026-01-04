#!/usr/bin/env python3
"""
Vote automation script using Selenium webdriver.
Accepts custom URLs and automates form submission by filling username and clicking vote button.
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class VoteAutomator:
    """Automates voting process using Selenium webdriver."""
    
    def __init__(self, url, username, timeout=10):
        """
        Initialize the vote automator.
        
        Args:
            url (str): The URL of the voting page
            username (str): Username to fill in the form
            timeout (int): Timeout for waiting for elements (default: 10 seconds)
        """
        self.url = url
        self.username = username
        self.timeout = timeout
        self.driver = None
    
    def start_driver(self):
        """Initialize the webdriver."""
        try:
            self.driver = webdriver.Chrome()
            print(f"✓ Chrome webdriver started successfully")
        except Exception as e:
            print(f"✗ Failed to start Chrome webdriver: {e}")
            sys.exit(1)
    
    def navigate_to_url(self):
        """Navigate to the voting page."""
        try:
            print(f"Navigating to {self.url}...")
            self.driver.get(self.url)
            print(f"✓ Successfully navigated to {self.url}")
        except Exception as e:
            print(f"✗ Failed to navigate to URL: {e}")
            self.close_driver()
            sys.exit(1)
    
    def fill_username_field(self):
        """
        Fill the username field in the voting form.
        
        Tries common username field identifiers (id, name, class).
        """
        try:
            # Wait for and find the username input field
            # Try multiple selectors in order of probability
            selectors = [
                (By.ID, "username"),
                (By.NAME, "username"),
                (By.CSS_SELECTOR, "input[type='text'][name='username']"),
                (By.CSS_SELECTOR, "input[type='text']"),
                (By.ID, "user"),
                (By.NAME, "user"),
            ]
            
            username_field = None
            for by, selector in selectors:
                try:
                    username_field = WebDriverWait(self.driver, self.timeout).until(
                        EC.presence_of_element_located((by, selector))
                    )
                    print(f"✓ Found username field using selector: {by.name}='{selector}'")
                    break
                except TimeoutException:
                    continue
            
            if username_field is None:
                raise NoSuchElementException("Could not find username field with any selector")
            
            # Clear any existing text and enter username
            username_field.clear()
            username_field.send_keys(self.username)
            print(f"✓ Successfully filled username field with: {self.username}")
            
        except Exception as e:
            print(f"✗ Failed to fill username field: {e}")
            self.close_driver()
            sys.exit(1)
    
    def click_vote_button(self):
        """
        Click the vote button.
        
        Tries common button identifiers and text patterns.
        """
        try:
            # Try multiple selectors for the vote button
            button_selectors = [
                (By.ID, "vote"),
                (By.NAME, "vote"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Vote')]"),
                (By.XPATH, "//button[contains(text(), 'vote')]"),
                (By.XPATH, "//input[@type='submit']"),
                (By.CSS_SELECTOR, "input[type='submit']"),
            ]
            
            vote_button = None
            for by, selector in button_selectors:
                try:
                    vote_button = WebDriverWait(self.driver, self.timeout).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    print(f"✓ Found vote button using selector: {by.name}='{selector}'")
                    break
                except TimeoutException:
                    continue
            
            if vote_button is None:
                raise NoSuchElementException("Could not find vote button with any selector")
            
            # Click the vote button
            vote_button.click()
            print("✓ Successfully clicked the vote button")
            
            # Wait a bit for the action to complete
            time.sleep(2)
            
        except Exception as e:
            print(f"✗ Failed to click vote button: {e}")
            self.close_driver()
            sys.exit(1)
    
    def close_driver(self):
        """Close the webdriver."""
        if self.driver:
            self.driver.quit()
            print("✓ Webdriver closed")
    
    def run(self):
        """Execute the complete voting automation process."""
        try:
            self.start_driver()
            self.navigate_to_url()
            self.fill_username_field()
            self.click_vote_button()
            print("\n✓ Voting process completed successfully!")
        except Exception as e:
            print(f"\n✗ Voting process failed: {e}")
            sys.exit(1)
        finally:
            self.close_driver()


def main():
    """Main entry point for the vote automation script."""
    if len(sys.argv) < 3:
        print("Usage: python vote.py <url> <username>")
        print("\nExample: python vote.py 'https://example.com/vote' 'john_doe'")
        print("\nArguments:")
        print("  url       - The URL of the voting page")
        print("  username  - Username to fill in the voting form")
        sys.exit(1)
    
    url = sys.argv[1]
    username = sys.argv[2]
    
    # Optional timeout parameter
    timeout = 10
    if len(sys.argv) > 3:
        try:
            timeout = int(sys.argv[3])
        except ValueError:
            print(f"✗ Invalid timeout value: {sys.argv[3]}")
            sys.exit(1)
    
    print("=" * 60)
    print("Vote Automation Script")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Username: {username}")
    print(f"Timeout: {timeout}s")
    print("=" * 60)
    
    # Create automator and run
    automator = VoteAutomator(url, username, timeout)
    automator.run()


if __name__ == "__main__":
    main()
