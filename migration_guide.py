#!/usr/bin/env python3
"""
How to Convert from FlareSolverr Server to Standalone
"""

# ============================================================
# OLD WAY: Using FlareSolverr Server
# ============================================================

"""
Before: You had to run a server in one terminal:

$ cd FlareSolverr
$ pip install -r requirements.txt
$ cd src
$ python flaresolverr.py

Then in another terminal, make HTTP requests:

import requests
import json

response = requests.post(
    'http://localhost:8191/v1',
    json={
        'cmd': 'request.get',
        'url': 'https://example.com',
        'maxTimeout': 60000
    }
)

data = response.json()
print(data['solution']['response'])
"""


# ============================================================
# NEW WAY: Using Standalone
# ============================================================

"""
Now: Just run the script directly in Python!
"""

from flaresolverr_standalone import StandaloneFlare

# Create instance (replaces running the server)
flare = StandaloneFlare(headless=True, timeout=60)

# Fetch URL (replaces HTTP POST request)
result = flare.fetch_url('https://example.com')

# Get data (replaces parsing JSON response)
html_content = result['html']
status_code = result['status']
cookies = result['cookies']
user_agent = result['user_agent']

flare.close()


# ============================================================
# MIGRATION GUIDE: Server Commands -> Standalone
# ============================================================

print("="*70)
print("MIGRATION GUIDE: FlareSolverr Server -> Standalone")
print("="*70)

# OLD: request.get
print("\n1. OLD: request.get")
print("-" * 70)
print("""
import requests

response = requests.post('http://localhost:8191/v1', json={
    'cmd': 'request.get',
    'url': 'https://example.com',
    'maxTimeout': 60000,
    'returnScreenshot': False
})

solution = response.json()['solution']
html = solution['response']
cookies = solution['cookies']
""")

print("NEW: request.get")
print("-" * 70)
print("""
from flaresolverr_standalone import StandaloneFlare

flare = StandaloneFlare(timeout=60)
result = flare.fetch_url('https://example.com')

html = result['html']
cookies = result['cookies']
flare.close()
""")


# OLD: request.post
print("\n2. OLD: request.post")
print("-" * 70)
print("""
import requests

response = requests.post('http://localhost:8191/v1', json={
    'cmd': 'request.post',
    'url': 'https://example.com',
    'postData': 'key=value&foo=bar',
    'maxTimeout': 60000
})

html = response.json()['solution']['response']
""")

print("NEW: request.post")
print("-" * 70)
print("""
from flaresolverr_standalone import StandaloneFlare
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

flare = StandaloneFlare()
result = flare.fetch_url('https://example.com')  # GET first

# For POST data, you'd need to modify the code to:
# 1. Fill form fields
# 2. Submit the form
# Or use Selenium's WebDriver directly

flare.close()
""")


# OLD: sessions
print("\n3. OLD: sessions (Create/List/Destroy)")
print("-" * 70)
print("""
import requests

# Create session
req = {
    'cmd': 'sessions.create',
    'session': 'my_session'
}
response = requests.post('http://localhost:8191/v1', json=req)

# Use session
req = {
    'cmd': 'request.get',
    'url': 'https://example.com',
    'session': 'my_session'
}
response = requests.post('http://localhost:8191/v1', json=req)

# Destroy session
req = {'cmd': 'sessions.destroy', 'session': 'my_session'}
requests.post('http://localhost:8191/v1', json=req)
""")

print("NEW: No sessions needed")
print("-" * 70)
print("""
from flaresolverr_standalone import StandaloneFlare

flare = StandaloneFlare()

# Each URL is independent - no session management needed
result1 = flare.fetch_url('https://site1.com')
result2 = flare.fetch_url('https://site2.com')

# Cookies are automatically managed per request

flare.close()
""")


# ============================================================
# BENEFITS OF STANDALONE
# ============================================================

print("\n" + "="*70)
print("BENEFITS OF STANDALONE")
print("="*70)

benefits = {
    "Simplicity": [
        "✓ No server to run",
        "✓ No port conflicts",
        "✓ No process management",
        "✓ Single Python script"
    ],
    "Integration": [
        "✓ Direct Python import",
        "✓ No HTTP overhead",
        "✓ Data stays in memory",
        "✓ Easy to integrate into scripts"
    ],
    "Debugging": [
        "✓ Can see browser for debugging",
        "✓ Full Python error messages",
        "✓ Easy to step through code",
        "✓ Direct logging"
    ],
    "Performance": [
        "✓ No network overhead",
        "✓ No JSON serialization",
        "✓ Direct data access",
        "✓ Faster for single requests"
    ]
}

for category, items in benefits.items():
    print(f"\n{category}:")
    for item in items:
        print(f"  {item}")


# ============================================================
# WHEN TO USE EACH
# ============================================================

print("\n" + "="*70)
print("WHEN TO USE EACH")
print("="*70)

print("""
USE STANDALONE WHEN:
  • You want to run directly in Python
  • You have a single script/app
  • You don't need persistent sessions
  • You want simplicity and speed
  • You're doing web scraping/crawling
  • You're integrating into existing Python code

USE SERVER WHEN:
  • You need HTTP API access
  • Multiple applications need to use it
  • You want persistent sessions
  • You need load balancing
  • You're running in Docker/containers
  • You need REST API endpoints
""")


# ============================================================
# EXAMPLE: Complete Web Scraper with Standalone
# ============================================================

print("\n" + "="*70)
print("EXAMPLE: Complete Web Scraper")
print("="*70)

from flaresolverr_standalone import StandaloneFlare
from bs4 import BeautifulSoup
import json
import csv
import time

def scrape_websites(urls, output_json='results.json', output_csv='results.csv'):
    """
    Complete example: Scrape multiple sites, bypass challenges, extract data
    """
    
    flare = StandaloneFlare(headless=True, disable_media=True, timeout=60)
    results = []
    
    print(f"\nScraping {len(urls)} websites...\n")
    
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}...", end=' ', flush=True)
        
        try:
            # Fetch with auto challenge bypass
            result = flare.fetch_url(url)
            
            if result['error'] is None:
                print("✓")
                
                # Parse HTML
                soup = BeautifulSoup(result['html'], 'html.parser')
                
                # Extract data
                data = {
                    'url': url,
                    'status': result['status'],
                    'title': soup.title.string if soup.title else 'N/A',
                    'links_count': len(soup.find_all('a')),
                    'images_count': len(soup.find_all('img')),
                    'cookies': len(result['cookies']),
                    'timestamp': result['timestamp'],
                    'error': None
                }
            else:
                print(f"✗ ({result['error']})")
                
                data = {
                    'url': url,
                    'status': result['status'],
                    'title': 'ERROR',
                    'links_count': 0,
                    'images_count': 0,
                    'cookies': 0,
                    'timestamp': result['timestamp'],
                    'error': result['error']
                }
            
            results.append(data)
            
            # Small delay between requests
            time.sleep(1)
        
        except Exception as e:
            print(f"✗ (Exception: {e})")
            results.append({
                'url': url,
                'status': 0,
                'title': 'ERROR',
                'links_count': 0,
                'images_count': 0,
                'cookies': 0,
                'timestamp': time.time(),
                'error': str(e)
            })
    
    flare.close()
    
    # Save as JSON
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save as CSV
    if results:
        with open(output_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    
    print(f"\nResults saved to {output_json} and {output_csv}")
    
    return results


# Example usage:
if __name__ == '__main__':
    example_urls = [
        'https://example.com',
        'https://httpbin.org/html',
    ]
    
    # Uncomment to run:
    # results = scrape_websites(example_urls)
    # for r in results:
    #     print(f"{r['url']}: {r['title']} ({r['links_count']} links)")


print("\nSee quick_start.py for more examples!")
