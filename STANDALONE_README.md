# Standalone FlareSolverr

A standalone Python script that bypasses Cloudflare and other challenges **without needing a server**. Reads URLs from a file, opens a browser, solves challenges, and stores data in variables.

## Key Features

- ✅ **No Server Required** - No localhost, no port listening, no sessions
- ✅ **Cloudflare Bypass** - Automatically detects and solves Cloudflare challenges
- ✅ **Single File** - Everything in one Python script
- ✅ **Easy to Use** - Read URLs from file, get results in variables
- ✅ **Data Storage** - Save results to JSON, access in memory
- ✅ **Headless & Visible** - Toggle browser visibility
- ✅ **Media Blocking** - Speed up with media disabled
- ✅ **Proxy Support** - Use with proxies if needed

## Installation

### 1. Install Python (3.9+)

```bash
python3 --version  # Should be 3.9 or higher
```

### 2. Install Dependencies

```bash
pip install -r requirements_standalone.txt
```

Or manually:

```bash
pip install selenium==4.39.0 undetected-chromedriver==3.5.4 certifi==2025.11.12
```

### 3. Install Chrome/Chromium

The script uses undetected-chromedriver which requires Chrome or Chromium to be installed.

**On Ubuntu/Debian:**
```bash
sudo apt-get install chromium-browser
# or
sudo apt-get install google-chrome-stable
```

**On macOS:**
```bash
brew install chromium
# or
brew install --cask google-chrome
```

**On Windows:**
Download from: https://www.google.com/chrome/

## Quick Start

### Method 1: Using the Built-in File Reader

1. Create a file `urls.txt` with URLs (one per line):
```
https://example.com
https://httpbin.org/delay/1
https://another-site.com
```

2. Run the script:
```bash
python3 flaresolverr_standalone.py
```

The script will:
- Open a browser
- Fetch each URL
- Bypass any Cloudflare challenges
- Save results to `results.json`

### Method 2: Use in Your Code

```python
from flaresolverr_standalone import StandaloneFlare

# Initialize
flare = StandaloneFlare(headless=False, timeout=60)

# Fetch a URL
result = flare.fetch_url('https://example.com')

# Access the data
print(result['status'])           # HTTP status
print(result['html'])              # Page HTML
print(result['cookies'])           # Extracted cookies
print(result['user_agent'])        # User agent used
print(result['error'])             # Any errors

flare.close()
```

## Usage Examples

### Example 1: Simple Single URL Fetch

```python
from flaresolverr_standalone import StandaloneFlare

flare = StandaloneFlare(headless=True)  # Hide browser
result = flare.fetch_url('https://httpbin.org/html')

if result['error'] is None:
    html = result['html']
    print(f"Got {len(html)} bytes of HTML")
else:
    print(f"Failed: {result['error']}")

flare.close()
```

### Example 2: Batch Processing from File

```python
from flaresolverr_standalone import StandaloneFlare

flare = StandaloneFlare(
    headless=True,           # Don't show browser
    disable_media=True,      # Faster - no images/css
    timeout=120              # 2 minute timeout per URL
)

# Read from file and fetch all
results = flare.fetch_from_file('urls.txt')

# Save to JSON
flare.save_results('output.json')

# Process results
for result in results:
    print(f"{result['url']}: {result['status']}")
    
    if result['error'] is None:
        # Store data in variables
        html_data = result['html']
        cookies = result['cookies']
        # Process further...

flare.close()
```

### Example 3: Access Data in Variables

```python
from flaresolverr_standalone import StandaloneFlare
import json

flare = StandaloneFlare()

# Fetch multiple URLs
flare.fetch_url('https://site1.com')
flare.fetch_url('https://site2.com')
flare.fetch_url('https://site3.com')

# Get all results as list
all_results = flare.get_all_results()

# Store in variables for processing
for i, result in enumerate(all_results):
    data = {
        'url': result['url'],
        'html': result['html'],
        'status': result['status'],
        'cookies': result['cookies'],
        'timestamp': result['timestamp']
    }
    
    # Use the data however you want
    print(f"Result {i+1}: {data['url']}")
    print(f"  Status: {data['status']}")
    print(f"  Cookies: {len(data['cookies'])}")

# Or convert to JSON string
json_str = json.dumps(all_results, indent=2)
print(json_str)

flare.close()
```

### Example 4: Extract Specific Information

```python
from flaresolverr_standalone import StandaloneFlare
from bs4 import BeautifulSoup

flare = StandaloneFlare(headless=True)

result = flare.fetch_url('https://example.com')

if result['error'] is None:
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(result['html'], 'html.parser')
    
    # Extract data
    title = soup.title.string if soup.title else 'No title'
    links = [a.get('href') for a in soup.find_all('a')]
    images = [img.get('src') for img in soup.find_all('img')]
    
    print(f"Title: {title}")
    print(f"Links: {links}")
    print(f"Images: {images}")

flare.close()
```

### Example 5: Custom Configuration

```python
from flaresolverr_standalone import StandaloneFlare

flare = StandaloneFlare(
    headless=False,           # Show the browser window
    disable_media=False,      # Load all resources
    timeout=180               # 3 minute timeout
)

result = flare.fetch_url('https://cloudflare-protected.com')

print(f"Status: {result['status']}")
print(f"User Agent: {result['user_agent']}")
print(f"Cookies found: {len(result['cookies'])}")

# Access cookies
for cookie in result['cookies']:
    print(f"  {cookie['name']} = {cookie['value'][:20]}...")

flare.close()
```

## API Reference

### StandaloneFlare Class

#### Constructor

```python
StandaloneFlare(headless=True, disable_media=False, timeout=60)
```

**Parameters:**
- `headless` (bool): Run browser in headless mode (default: True)
- `disable_media` (bool): Block images/CSS/fonts to speed up (default: False)
- `timeout` (int): Max seconds to wait per URL (default: 60)

#### Methods

##### fetch_url(url, timeout=None)
Fetch a single URL and bypass challenges.

```python
result = flare.fetch_url('https://example.com', timeout=120)
```

**Returns:** Dictionary with keys:
- `url`: The URL fetched
- `status`: HTTP status code
- `html`: Full page HTML
- `cookies`: List of cookies
- `user_agent`: Browser user agent
- `error`: Error message (None if successful)
- `timestamp`: When it was fetched

##### fetch_from_file(filename, timeout=None)
Read URLs from file and fetch each one.

```python
results = flare.fetch_from_file('urls.txt', timeout=120)
```

**File format:**
```
https://site1.com
https://site2.com
# Comments are supported
https://site3.com
```

##### save_results(output_file='results.json')
Save all results to JSON file.

```python
flare.save_results('my_results.json')
```

##### get_html(url_index=0)
Get HTML content from a specific result.

```python
html = flare.get_html(0)  # First result
```

##### get_all_results()
Get all results as a list.

```python
all_results = flare.get_all_results()
for result in all_results:
    print(result['url'], result['status'])
```

##### close()
Close the browser and cleanup.

```python
flare.close()
```

## Data Structure

Each result is a dictionary:

```python
{
    'url': 'https://example.com',
    'status': 200,
    'html': '<html>...</html>',
    'cookies': [
        {
            'name': 'cookie_name',
            'value': 'cookie_value',
            'domain': '.example.com',
            'path': '/',
            'expires': 1735689600,
            'httpOnly': True,
            'secure': True,
            'sameSite': 'Lax'
        }
    ],
    'user_agent': 'Mozilla/5.0...',
    'error': None,  # None if successful
    'timestamp': 1672531200.123
}
```

## Common Issues

### Issue: "Chrome not found"

**Solution:** Install Chrome/Chromium:
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# macOS
brew install chromium

# Windows: Download from https://www.google.com/chrome/
```

### Issue: "Permission denied"

**Solution:** Make script executable:
```bash
chmod +x flaresolverr_standalone.py
```

### Issue: Timeout errors

**Solution:** Increase timeout:
```python
flare = StandaloneFlare(timeout=180)  # 3 minutes
```

### Issue: "Undetected Chrome failed"

**Solution:** Update packages:
```bash
pip install --upgrade undetected-chromedriver selenium
```

## Performance Tips

1. **Disable Media** - Much faster:
   ```python
   flare = StandaloneFlare(disable_media=True)
   ```

2. **Use Headless Mode** - Faster and uses less memory:
   ```python
   flare = StandaloneFlare(headless=True)
   ```

3. **Batch Processing** - Process multiple URLs:
   ```python
   flare.fetch_from_file('urls.txt')  # Processes with delays
   ```

4. **Set Timeout** - Don't wait forever:
   ```python
   flare = StandaloneFlare(timeout=30)  # 30 seconds max
   ```

## Comparison with FlareSolverr Server

| Feature | Server | Standalone |
|---------|--------|-----------|
| Localhost | ✓ | ✗ |
| HTTP API | ✓ | ✗ |
| Sessions | ✓ | ✗ |
| Single File | ✗ | ✓ |
| Easy Setup | ~ | ✓ |
| In-Memory Data | ~ | ✓ |
| No Dependencies | ✗ | ✗ |
| Python Integration | ~ | ✓ |

## Advanced Usage

### Combine with BeautifulSoup for Web Scraping

```python
from flaresolverr_standalone import StandaloneFlare
from bs4 import BeautifulSoup

flare = StandaloneFlare(disable_media=True)

results = flare.fetch_from_file('urls.txt')

for result in results:
    if result['error'] is None:
        soup = BeautifulSoup(result['html'], 'html.parser')
        # Extract data...
        
flare.close()
```

### Proxy Support

```python
from flaresolverr_standalone import StandaloneFlare
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

# Note: Current version uses undetected-chromedriver
# For proxy support, would need to use standard Selenium
# This is a future enhancement
```

## License

This script is based on FlareSolverr (https://github.com/FlareSolverr/FlareSolverr)
Used under the MIT License.

## Support

For issues specific to this standalone version, check the code comments.
For Cloudflare bypass issues, see: https://github.com/FlareSolverr/FlareSolverr

---

**Note:** This is a standalone Python implementation. For server-based deployment, use the official FlareSolverr project.
