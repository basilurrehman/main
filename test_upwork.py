from flaresolverr_standalone import StandaloneFlare

flare = StandaloneFlare(headless=False, timeout=120)  # 2 minute timeout

result = flare.fetch_url('https://www.upwork.com/nx/search/jobs/?category2_uid=531770282580668418&q=(www.%20OR%20.com%20OR%20https)&page=1&per_page=50')

print(f"\nStatus: {result['status']}")
print(f"Error: {result['error']}")
print(f"HTML length: {len(result['html']) if result['html'] else 0}")
print(f"Title from HTML: ", end="")
if result['html']:
    import re
    match = re.search(r'<title>(.*?)</title>', result['html'])
    print(match.group(1) if match else "Not found")

flare.close()
