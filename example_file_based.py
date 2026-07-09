#!/usr/bin/env python3
"""
Example: Read URLs from file and fetch them with FlareSolverr standalone
"""

from flaresolverr_standalone import StandaloneFlare

# Initialize FlareSolverr
flare = StandaloneFlare(headless=True)

# Read URLs from file
urls = []
with open('urls_to_fetch.txt', 'r') as f:
    for line in f:
        url = line.strip()
        if url and not url.startswith('#'):
            urls.append(url)

print(f"Found {len(urls)} URLs to fetch\n")

# Fetch each URL and store results in variables
results = {}
for url in urls:
    try:
        print(f"Fetching: {url}")
        result = flare.fetch_url(url)
        results[url] = {
            'status': result.get('status'),
            'html_length': len(result.get('html', '')),
            'html': result.get('html', '')
        }
        print(f"✓ Success - HTML length: {results[url]['html_length']}\n")
    except Exception as e:
        print(f"✗ Failed: {e}\n")
        results[url] = {'status': 'error', 'error': str(e)}

# Close browser
flare.close()

# Now you have all data in 'results' variable
print("\n=== RESULTS STORED IN MEMORY ===")
for url, data in results.items():
    if data.get('status') == 'ok':
        print(f"{url}: SUCCESS ({data['html_length']} bytes)")
    else:
        print(f"{url}: FAILED - {data.get('error')}")

# You can access the data without server/localhost
print("\n=== ACCESSING DATA ===")
print(f"First result HTML preview: {results[urls[0]]['html'][:200]}...")
