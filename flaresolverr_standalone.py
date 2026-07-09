#!/usr/bin/env python3
"""
Standalone FlareSolverr - Bypass Cloudflare and other challenges without server
Reads URLs from a file, bypasses protection, and stores data in variables
"""

import json
import logging
import os
import time
import sys
import platform
import re
import certifi
from datetime import timedelta
from urllib.parse import urlparse
from subprocess import check_output

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located, title_is, staleness_of
)
import undetected_chromedriver as uc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set SSL certificates for requests
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()

# Challenge detection patterns
ACCESS_DENIED_TITLES = [
    'Access denied',
    'Attention Required! | Cloudflare'
]

ACCESS_DENIED_SELECTORS = [
    'div.cf-error-title span.cf-code-label span',
    '#cf-error-details div.cf-error-overview h1'
]

CHALLENGE_TITLES = [
    'Just a moment...',
    'DDoS-Guard'
]

CHALLENGE_SELECTORS = [
    '#cf-challenge-running', '.ray_id', '.attack-box', '#cf-please-wait', 
    '#challenge-spinner', '#trk_jschal_js', '#turnstile-wrapper', '.lds-ring',
    'td.info #js_info',
    'div.vc div.text-box h2'
]

TURNSTILE_SELECTORS = [
    "input[name='cf-turnstile-response']"
]

SHORT_TIMEOUT = 1
# Increased timeout for challenge resolution (matching FlareSolverr)
CHALLENGE_TIMEOUT = 8


def get_chrome_exe_path():
    """Get Chrome/Chromium executable path"""
    if os.name == 'nt':
        # Windows
        paths = [
            os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
            os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
            os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe'),
        ]
    else:
        # Linux/macOS
        paths = [
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/snap/bin/chromium',
        ]
    
    for path in paths:
        if os.path.exists(path):
            return path
    
    return 'google-chrome'


def get_chrome_major_version():
    """Get the major version of Chrome/Chromium installed"""
    try:
        chrome_path = get_chrome_exe_path()
        if os.name == 'nt':
            # Windows - get version from file properties
            output = check_output([chrome_path, '--version']).decode().strip()
        else:
            # Linux/macOS - get version from command line
            process = os.popen(f'"{chrome_path}" --version')
            output = process.read().strip()
        
        # Extract version number (e.g., "Google Chrome 134.0.6998.88" -> "134")
        match = re.search(r'(\d+)', output)
        if match:
            major_version = int(match.group(1))
            logger.debug(f"Detected Chrome version: {output}, major version: {major_version}")
            return major_version
        return None
    except Exception as e:
        logger.debug(f"Could not detect Chrome version: {e}")
        return None


class StandaloneFlare:
    """Standalone FlareSolverr without server"""
    
    def __init__(self, headless=True, disable_media=False, timeout=60):
        """
        Initialize the standalone FlareSolverr
        
        Args:
            headless: Run browser in headless mode (default: True)
            disable_media: Block images, CSS, fonts (default: False)
            timeout: Maximum time to wait for challenge resolution in seconds (default: 60)
        """
        self.headless = headless
        self.disable_media = disable_media
        self.timeout = timeout
        self.driver = None
        self.results = []
        
    def _create_driver(self):
        """Create and return an undetected Chrome webdriver"""
        try:
            logger.info("Creating undetected Chrome webdriver...")
            options = uc.ChromeOptions()
            
            # Match FlareSolverr options
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-search-engine-choice-screen')
            options.add_argument('--disable-setuid-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-zygote')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            if self.headless:
                options.add_argument('--headless')
            
            # Get Chrome version to match with ChromeDriver
            browser_exe_path = get_chrome_exe_path()
            version_main = get_chrome_major_version()
            
            logger.info(f"Chrome executable: {browser_exe_path}, version: {version_main}")
            
            # Create driver with matched version
            driver = uc.Chrome(
                options=options,
                browser_executable_path=browser_exe_path,
                version_main=version_main
            )
            logger.info("WebDriver created successfully")
            return driver
        except Exception as e:
            logger.error(f"Failed to create webdriver: {e}")
            raise
    
    def _click_verify(self, driver, num_tabs=1):
        """Attempt to click the Cloudflare verify button"""
        try:
            logger.debug("Attempting to click Cloudflare verify checkbox...")
            actions = ActionChains(driver)
            actions.pause(5)
            for _ in range(num_tabs):
                actions.send_keys(Keys.TAB).pause(0.1)
            actions.pause(1)
            actions.send_keys(Keys.SPACE).perform()
            logger.debug(f"Verify checkbox clicked after {num_tabs} tabs")
        except Exception as e:
            logger.debug(f"Could not click verify checkbox: {e}")
        finally:
            try:
                driver.switch_to.default_content()
            except:
                pass
        
        # Try to find and click the "Verify you are human" button
        try:
            logger.debug("Looking for 'Verify you are human' button...")
            button = driver.find_element(
                by=By.XPATH,
                value="//input[@type='button' and @value='Verify you are human']",
            )
            if button:
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(button, 5, 7)
                actions.click(button)
                actions.perform()
                logger.debug("Clicked 'Verify you are human' button")
        except Exception as e:
            logger.debug(f"'Verify you are human' button not found: {e}")
        
        time.sleep(2)
        logger.debug("Waited 2 seconds after click_verify")
    
    def _get_turnstile_token(self, driver, tabs=1):
        """Extract Turnstile token from the page"""
        try:
            token_input = driver.find_element(By.CSS_SELECTOR, "input[name='cf-turnstile-response']")
            current_value = token_input.get_attribute("value")
            
            while True:
                self._click_verify(driver, num_tabs=tabs)
                turnstile_token = token_input.get_attribute("value")
                
                if turnstile_token and turnstile_token != current_value:
                    logger.info(f"Turnstile token obtained: {turnstile_token[:20]}...")
                    return turnstile_token
                
                logger.debug("Retrying token extraction...")
                
                # Reset focus
                driver.execute_script("""
                    let el = document.createElement('button');
                    el.style.position='fixed';
                    el.style.top='0';
                    el.style.left='0';
                    document.body.prepend(el);
                    el.focus();
                """)
                time.sleep(1)
        except Exception as e:
            logger.debug(f"Could not extract Turnstile token: {e}")
            return None
    
    def _bypass_challenge(self, driver):
        """Wait for and bypass Cloudflare challenge.

        This method will try to resolve detected challenges until the overall
        `self.timeout` (seconds) is reached. It logs progress and raises an
        exception on timeout or access denied.
        """
        logger.info("Checking for challenges...")

        start_ts = time.time()

        def time_left():
            return max(0, self.timeout - (time.time() - start_ts))

        page_title = driver.title
        logger.debug(f"Page title: {page_title}")

        # Check for access denied
        for title in ACCESS_DENIED_TITLES:
            if page_title.startswith(title):
                raise Exception(f"Access denied: {title}")

        for selector in ACCESS_DENIED_SELECTORS:
            found = driver.find_elements(By.CSS_SELECTOR, selector)
            if found:
                raise Exception(f"Access denied by selector: {selector}")

        # Check for challenges
        challenge_found = False
        for title in CHALLENGE_TITLES:
            if title.lower() == page_title.lower():
                challenge_found = True
                logger.info(f"Challenge detected by title: {page_title}")
                break

        if not challenge_found:
            for selector in CHALLENGE_SELECTORS:
                found = driver.find_elements(By.CSS_SELECTOR, selector)
                if found:
                    challenge_found = True
                    logger.info(f"Challenge detected by selector: {selector}")
                    break

        if not challenge_found:
            # nothing to do
            logger.debug("No challenge detected")
            return

        logger.info("Resolving challenge...")
        attempt = 0

        while time_left() > 0:
            attempt += 1
            logger.debug(f"Challenge resolution attempt {attempt}, time left: {time_left():.1f}s")

            try:
                # Wait for title to change from challenge titles
                for title in CHALLENGE_TITLES:
                    WebDriverWait(driver, min(CHALLENGE_TIMEOUT, time_left())).until_not(title_is(title))

                # Wait for all challenge selectors to disappear
                for selector in CHALLENGE_SELECTORS:
                    WebDriverWait(driver, min(CHALLENGE_TIMEOUT, time_left())).until_not(
                        presence_of_element_located((By.CSS_SELECTOR, selector))
                    )

                # If we reach here without exceptions, challenge cleared
                logger.info("Challenge resolved!")
                # Wait for full document readiness before returning
                try:
                    ready_left = min(5, time_left())
                    WebDriverWait(driver, ready_left).until(lambda d: d.execute_script("return document.readyState") == 'complete')
                    logger.debug("Document readyState is 'complete'")
                except Exception:
                    logger.debug("Document did not reach 'complete' state within short wait")
                return

            except TimeoutException:
                logger.debug(f"Attempt {attempt} timed out waiting for challenge to clear; trying interactive actions")
                # Try interactive clicks/keyboard to progress challenge
                try:
                    self._click_verify(driver)
                except Exception:
                    logger.debug("click_verify raised an exception")

                # After interactive attempt, wait briefly for possible redirect/reload
                logger.debug("Waiting shortly for possible redirect/reload...")
                try:
                    html_element = driver.find_element(By.TAG_NAME, "html")
                    WebDriverWait(driver, min(CHALLENGE_TIMEOUT, time_left())).until(staleness_of(html_element))
                    logger.debug("Page became stale (redirect/reload detected)")
                except TimeoutException:
                    logger.debug("No redirect detected after interactive action")

        # If we get here, overall timeout expired
        raise Exception(f'Error solving the challenge. Timeout after {self.timeout} seconds.')
    
    def fetch_url(self, url, timeout=None):
        """
        Fetch a single URL and bypass Cloudflare challenges
        
        Args:
            url: URL to fetch
            timeout: Optional timeout override (in seconds)
        
        Returns:
            Dictionary with result data
        """
        if timeout is None:
            timeout = self.timeout
        
        result = {
            'url': url,
            'status': None,
            'html': None,
            'cookies': [],
            'user_agent': None,
            'error': None,
            'timestamp': time.time()
        }
        
        try:
            if self.driver is None:
                self.driver = self._create_driver()
            
            logger.info(f"Fetching: {url}")
            
            # Block resources if needed
            if self.disable_media:
                try:
                    block_urls = [
                        "*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp", "*.css",
                        "*.woff", "*.woff2", "*.ttf", "*.otf"
                    ]
                    self.driver.execute_cdp_cmd("Network.enable", {})
                    self.driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": block_urls})
                    logger.debug("Media blocking enabled")
                except Exception as e:
                    logger.debug(f"Could not enable media blocking: {e}")
            
            # Navigate to URL
            self.driver.get(url)
            
            # Bypass challenges
            self._bypass_challenge(self.driver)
            
            # Extract data
            result['status'] = 200
            result['html'] = self.driver.page_source
            result['user_agent'] = self.driver.execute_script("return navigator.userAgent")
            
            # Get cookies
            for cookie in self.driver.get_cookies():
                result['cookies'].append({
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    'domain': cookie.get('domain'),
                    'path': cookie.get('path'),
                    'expires': cookie.get('expiry'),
                    'httpOnly': cookie.get('httpOnly'),
                    'secure': cookie.get('secure'),
                    'sameSite': cookie.get('sameSite')
                })
            
            logger.info(f"Successfully fetched {url}")
            
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            result['error'] = str(e)
            result['status'] = 0
        
        self.results.append(result)
        return result
    
    def fetch_from_file(self, filename, timeout=None):
        """
        Read URLs from a file and fetch each one
        
        Args:
            filename: Path to file containing URLs (one per line)
            timeout: Optional timeout override (in seconds)
        
        Returns:
            List of result dictionaries
        """
        if not os.path.exists(filename):
            logger.error(f"File not found: {filename}")
            return []
        
        try:
            with open(filename, 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            logger.info(f"Found {len(urls)} URLs in {filename}")
            
            for url in urls:
                # Ensure URL has protocol
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                self.fetch_url(url, timeout)
                # Add delay between requests
                time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error reading file {filename}: {e}")
        
        return self.results
    
    def save_results(self, output_file='results.json'):
        """
        Save results to JSON file
        
        Args:
            output_file: Path to output JSON file
        """
        try:
            # Prepare data for JSON serialization
            data = []
            for result in self.results:
                item = {
                    'url': result['url'],
                    'status': result['status'],
                    'user_agent': result['user_agent'],
                    'cookies_count': len(result['cookies']),
                    'cookies': result['cookies'],
                    'error': result['error'],
                    'timestamp': result['timestamp'],
                    'html_length': len(result['html']) if result['html'] else 0
                }
                data.append(item)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def get_html(self, url_index=0):
        """Get HTML content from a specific result"""
        if 0 <= url_index < len(self.results):
            return self.results[url_index]['html']
        return None
    
    def get_all_results(self):
        """Get all results"""
        return self.results
    
    def close(self):
        """Close the webdriver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver closed")
            except Exception as e:
                logger.error(f"Error closing webdriver: {e}")
            finally:
                self.driver = None
    
    def __del__(self):
        """Cleanup on object deletion"""
        self.close()


def main():
    """Main function - example usage"""
    
    # Create input file with URLs
    urls_file = 'urls.txt'
    
    # Check if file exists, if not create example
    if not os.path.exists(urls_file):
        logger.info(f"Creating example {urls_file}...")
        with open(urls_file, 'w') as f:
            f.write("""# List of URLs to fetch (one per line)
# Lines starting with # are comments
https://www.example.com
https://www.httpbin.org/delay/1
https://www.cloudflare.com
""")
        logger.info(f"Created {urls_file} - please add your URLs and run again")
        return
    
    # Initialize FlareSolverr
    flare = StandaloneFlare(
        headless=False,  # Set to False to see the browser
        disable_media=True,  # Block images and CSS to speed up
        timeout=60  # 60 seconds timeout per URL
    )
    
    try:
        # Fetch URLs from file
        results = flare.fetch_from_file(urls_file)
        
        # Save results
        flare.save_results('results.json')
        
        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        for i, result in enumerate(results):
            status = "✓" if result['error'] is None else "✗"
            print(f"{status} [{i+1}] {result['url']}")
            if result['error']:
                print(f"    Error: {result['error']}")
            else:
                print(f"    Status: {result['status']}")
                print(f"    Cookies: {len(result['cookies'])}")
                print(f"    HTML size: {len(result['html'])} bytes")
        
        # Access results programmatically
        print("\n" + "="*60)
        print("ACCESSING RESULTS")
        print("="*60)
        print(f"Total results: {len(flare.get_all_results())}")
        
        # Example: Get HTML from first successful result
        for result in flare.get_all_results():
            if result['error'] is None:
                html = result['html']
                print(f"\nFirst {100} characters of {result['url']}:")
                print(html[:100] + "...")
                break
    
    finally:
        # Always close the browser
        flare.close()


if __name__ == '__main__':
    main()
