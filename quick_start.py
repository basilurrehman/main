#!/usr/bin/env python3
"""
Quick Start Guide - Copy and paste examples to run immediately
"""

# ============================================================
# QUICK START #1: Fetch ONE URL
# ============================================================

from flaresolverr_standalone import StandaloneFlare

flare = StandaloneFlare(headless=False)  # headless=True to hide browser
result = flare.fetch_url('https://httpbin.org/html')

print("Status:", result['status'])
print("HTML length:", len(result['html']) if result['html'] else 0)
print("Cookies:", len(result['cookies']))
print("Error:", result['error'])

# Save HTML to file
if result['html']:
    with open('page.html', 'w') as f:
        f.write(result['html'])

flare.close()


# ============================================================
# QUICK START #2: Fetch from FILE
# ============================================================

from flaresolverr_standalone import StandaloneFlare

# First, create a file called 'urls.txt' with your URLs:
# https://example.com
# https://httpbin.org/html
# https://another-site.com

flare = StandaloneFlare(headless=True, disable_media=True)

# Fetch all URLs from file
results = flare.fetch_from_file('urls.txt')

# Save results to JSON
flare.save_results('results.json')

# Print summary
for result in results:
    print(f"{result['url']}: {result['status']} - Error: {result['error']}")

flare.close()


# ============================================================
# QUICK START #3: Access DATA in Variables
# ============================================================

from flaresolverr_standalone import StandaloneFlare

flare = StandaloneFlare()

result = flare.fetch_url('https://httpbin.org/html')

# All data in variables - use it however you want!
url = result['url']
status = result['status']
html = result['html']
cookies = result['cookies']
error = result['error']
user_agent = result['user_agent']
timestamp = result['timestamp']

# Do something with the data
if error is None:
    print(f"Successfully fetched {url}")
    print(f"Got {len(html)} characters of HTML")
    print(f"Got {len(cookies)} cookies")
    
    # Save HTML
    with open(f'html_{url.replace("https://", "").replace("/", "_")}.html', 'w') as f:
        f.write(html)
    
    # Save cookies as JSON
    import json
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f, indent=2)

flare.close()


# ============================================================
# QUICK START #4: Process Multiple URLs with Loop
# ============================================================

from flaresolverr_standalone import StandaloneFlare
import json

flare = StandaloneFlare(headless=True)

urls = [
    'https://example.com',
    'https://httpbin.org/html',
]

all_data = []

for url in urls:
    result = flare.fetch_url(url)
    
    # Store in list
    all_data.append({
        'url': result['url'],
        'status': result['status'],
        'html_size': len(result['html']) if result['html'] else 0,
        'cookies_count': len(result['cookies']),
        'error': result['error']
    })

# Save all to JSON
with open('all_data.json', 'w') as f:
    json.dump(all_data, f, indent=2)

print(f"Processed {len(all_data)} URLs")

flare.close()


# ============================================================
# QUICK START #5: Parse HTML and Extract Data
# ============================================================

from flaresolverr_standalone import StandaloneFlare
from html.parser import HTMLParser

flare = StandaloneFlare(headless=True)

result = flare.fetch_url('https://httpbin.org/html')

if result['error'] is None:
    html = result['html']
    
    # Simple text extraction (without HTML tags)
    class TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = []
        
        def handle_data(self, data):
            text = data.strip()
            if text:
                self.text.append(text)
        
        def get_text(self):
            return ' '.join(self.text)
    
    extractor = TextExtractor()
    extractor.feed(html)
    text = extractor.get_text()
    
    print("Extracted text (first 200 chars):")
    print(text[:200])

flare.close()


# ============================================================
# QUICK START #6: With Error Handling
# ============================================================

from flaresolverr_standalone import StandaloneFlare

def safe_fetch(url, max_retries=3):
    """Fetch URL with retry logic"""
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}: {url}")
            
            flare = StandaloneFlare(headless=True, timeout=60)
            result = flare.fetch_url(url)
            flare.close()
            
            if result['error'] is None:
                print(f"✓ Success!")
                return result
            else:
                print(f"✗ Error: {result['error']}")
        
        except Exception as e:
            print(f"✗ Exception: {e}")
        
        if attempt < max_retries - 1:
            import time
            time.sleep(2)  # Wait before retry
    
    return None

# Usage
result = safe_fetch('https://example.com')

if result:
    print(f"Got {len(result['html'])} bytes of HTML")
else:
    print("Failed to fetch after retries")


# ============================================================
# QUICK START #7: Export Results in Different Formats
# ============================================================

from flaresolverr_standalone import StandaloneFlare
import json
import csv

flare = StandaloneFlare(headless=True)

# Fetch some URLs
results = flare.fetch_from_file('urls.txt')

# Export as JSON
with open('results.json', 'w') as f:
    json.dump([{
        'url': r['url'],
        'status': r['status'],
        'error': r['error'],
        'timestamp': r['timestamp']
    } for r in results], f, indent=2)

# Export as CSV
with open('results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['url', 'status', 'error', 'timestamp'])
    writer.writeheader()
    for r in results:
        writer.writerow({
            'url': r['url'],
            'status': r['status'],
            'error': r['error'],
            'timestamp': r['timestamp']
        })

print(f"Exported {len(results)} results to results.json and results.csv")

flare.close()


# ============================================================
# QUICK START #8: Monitor Progress
# ============================================================

from flaresolverr_standalone import StandaloneFlare
import time

flare = StandaloneFlare(headless=True)

urls = [
    'https://example.com',
    'https://httpbin.org/html',
    'https://httpbin.org/delay/1',
]

start_time = time.time()
successful = 0
failed = 0

for i, url in enumerate(urls, 1):
    print(f"[{i}/{len(urls)}] Fetching {url}...", end=' ', flush=True)
    
    result = flare.fetch_url(url)
    
    if result['error'] is None:
        print("✓")
        successful += 1
    else:
        print(f"✗ ({result['error']})")
        failed += 1

elapsed = time.time() - start_time

print(f"\n{'='*60}")
print(f"Results: {successful} successful, {failed} failed")
print(f"Time: {elapsed:.1f} seconds")
print(f"Average: {elapsed/len(urls):.1f} seconds per URL")
print(f"{'='*60}")

flare.close()
