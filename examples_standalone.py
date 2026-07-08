#!/usr/bin/env python3
"""
Simple usage examples for standalone FlareSolverr
"""

from flaresolverr_standalone import StandaloneFlare
import json


# EXAMPLE 1: Fetch single URL
print("=" * 60)
print("EXAMPLE 1: Fetch a single URL")
print("=" * 60)

flare = StandaloneFlare(headless=False, timeout=60)

result = flare.fetch_url('https://www.example.com')

print(f"URL: {result['url']}")
print(f"Status: {result['status']}")
print(f"Error: {result['error']}")
print(f"HTML length: {len(result['html']) if result['html'] else 0}")
print(f"Cookies: {result['cookies']}")

flare.close()


# EXAMPLE 2: Fetch from file
print("\n" + "=" * 60)
print("EXAMPLE 2: Fetch URLs from file")
print("=" * 60)

# Create sample file
with open('urls_sample.txt', 'w') as f:
    f.write("""https://example.com
https://httpbin.org/delay/1
""")

flare = StandaloneFlare(headless=True, disable_media=True, timeout=60)
results = flare.fetch_from_file('urls_sample.txt')
flare.save_results('results_sample.json')

print(f"Fetched {len(results)} URLs")
for result in results:
    print(f"  - {result['url']}: {result['status']} (error: {result['error']})")

flare.close()


# EXAMPLE 3: Access data directly in variables
print("\n" + "=" * 60)
print("EXAMPLE 3: Access data in variables")
print("=" * 60)

flare = StandaloneFlare(headless=True)

# Fetch URL
flare.fetch_url('https://httpbin.org/html')

# Get all results
all_results = flare.get_all_results()
print(f"Total results: {len(all_results)}")

# Get HTML from first result
html_content = flare.get_html(0)
if html_content:
    print(f"HTML preview: {html_content[:200]}...")
    
    # Parse and manipulate HTML
    from html.parser import HTMLParser
    
    class MLStripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self.reset()
            self.strict = False
            self.convert_charrefs = True
            self.text = []
        
        def handle_data(self, d):
            self.text.append(d)
        
        def get_data(self):
            return ''.join(self.text)
    
    stripper = MLStripper()
    stripper.feed(html_content)
    text = stripper.get_data()
    print(f"Text content: {text[:200]}...")

flare.close()


# EXAMPLE 4: Custom configuration
print("\n" + "=" * 60)
print("EXAMPLE 4: Custom configuration")
print("=" * 60)

flare = StandaloneFlare(
    headless=False,  # Show browser
    disable_media=True,  # Don't load images/css
    timeout=120  # 2 minute timeout
)

result = flare.fetch_url('https://example.com')

# Access various data
print(f"URL: {result['url']}")
print(f"Status: {result['status']}")
print(f"User Agent: {result['user_agent']}")
print(f"Cookies count: {len(result['cookies'])}")

# Print all cookies
if result['cookies']:
    print("\nCookies:")
    for cookie in result['cookies']:
        print(f"  {cookie['name']} = {cookie['value']}")

flare.close()
