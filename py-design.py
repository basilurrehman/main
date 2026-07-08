import sys
import re
import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding="utf-8")
EXCLUDED_DOMAINS = [
    "github.com", "githubassets.com", "wixpress.com", "mailchimp.com", "wordpress.com",
    "domain.com",
    "no-reply.com",
    "example.com",
    "sentry.io",
    "sentry.com", "figma.com"
]

LANGUAGE_KEYWORDS = {
    'contact': ['contact', 'contacto', 'kontakt', 'контакт', 'contatto', 'kontakt'],
    'about': ['about', 'acerca de', 'propos', 'über', 'informazioni', 'sobre', 'nas', 'over', 'support', 'get-to-know-us', 'quiénes-somos', 'quienes-somos', 'get in touch', 'getintouch', 'get-in-touch', 'support']
}

def is_valid_email(email):
    email_regex = (
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.'  
        r'(com|edu|gov|org|in|co|net|biz|online|tech|info|io|ai|app|dev|xyz|store|design|us|uk|ca|au|de|fr|es|it|jp|cn|com\.in|co\.uk)'
        r'(\.[a-zA-Z]{2,})?$'
    )
    return re.match(email_regex, email)

def extract_emails(content):
    raw_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
    valid_emails = set(email for email in raw_emails if is_valid_email(email) and not any(domain in email for domain in EXCLUDED_DOMAINS))
    
    mailto_emails = re.findall(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', content)
    valid_emails.update(mailto_emails)
    
    return valid_emails

def extract_phone_numbers(soup):
    # Extract visible text from the HTML document
    visible_text = soup.get_text(separator=" ", strip=True)

    # Regular expression to find phone numbers in plain text
    phone_number_pattern = r'(?<!\w)(?:\+\d{1,3}[-.\s]?)?(?:\(\d{1,4}\)[-\s]?)?\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{2,9}(?!\w)'
    
    # Find all phone numbers in the visible text
    phone_numbers = re.findall(phone_number_pattern, visible_text)
    
    # Remove duplicates and return
    return list(set(phone_numbers))



def extract_social_links(base_url, soup):
    social_links = {
        "instagram": [],
        "linkedin": [],
        "facebook": [],
        "twitter": [],
        "whatsapp": []
    }

    for tag in soup.find_all('a', href=True):
        link = urljoin(base_url, tag['href'])
        parsed_link = urlparse(link)
        domain = parsed_link.netloc.lower()
        path = parsed_link.path.lower()

        if "instagram.com" in domain and path.strip("/") and "/p/" not in path:
            social_links["instagram"].append(link)
        elif "linkedin.com" in domain and ("/in/" in path or "/company/" in path):
            social_links["linkedin"].append(link)
        elif "facebook.com" in domain and path.strip("/") and not any(x in path for x in ["/share/", "/sharer.php", "/share.php", "/photo/", "/video/"]):
            social_links["facebook"].append(link)
        elif "twitter.com" in domain and path.strip("/") and "/status/" not in path:
            social_links["twitter"].append(link)
        elif "wa.me" in domain or "whatsapp.com" in domain:
            social_links["whatsapp"].append(link)

    return social_links

def get_relevant_links(base_url, soup):
    base_domain = urlparse(base_url).netloc
    relevant_links = set()

    for tag in soup.find_all('a', href=True):
        link = urljoin(base_url, tag['href'])
        link_path = urlparse(link).path.lower()

        if urlparse(link).netloc == base_domain:
            if any(keyword in link_path for keyword in LANGUAGE_KEYWORDS['contact']) or \
               any(keyword in link_path for keyword in LANGUAGE_KEYWORDS['about']):
                relevant_links.add(link)

    return list(relevant_links)

def extract_company_names(soup):
    company_names = set()

    # Extract from meta tags
    for meta in soup.find_all('meta', attrs={'property': 'og:site_name'}):
        if meta.get('content'):
            company_names.add(meta.get('content'))

    for meta in soup.find_all('meta', attrs={'name': 'og:company'}):
        if meta.get('content'):
            company_names.add(meta.get('content'))

    # Extract from the full title tag
    title_tag = soup.find('title')
    if title_tag:
        title_text = title_tag.get_text().strip()
        company_names.add(title_text)

    # Extract from JSON-LD script
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get('@type') == 'Organization':
                if 'name' in data:
                    company_names.add(data['name'])
        except (json.JSONDecodeError, TypeError):
            continue
            
    # Extract from image alt texts that contain the word "logo"
    for img in soup.find_all('img', alt=True):
        if 'logo' in img['alt'].lower():
            company_names.add(img['alt'].strip())

    return list(company_names)

def longest_common_substring_with_exceptions(str1, str2):
    clean_str1 = re.sub(r'[^a-zA-Z0-9]', '', str1)
    clean_str2 = re.sub(r'[^a-zA-Z0-9]', '', str2)
    
    max_len = 0
    end_pos = 0
    lcs_table = [[0] * (len(clean_str2) + 1) for _ in range(len(clean_str1) + 1)]

    for i in range(1, len(clean_str1) + 1):
        for j in range(1, len(clean_str2) + 1):
            if clean_str1[i - 1].lower() == clean_str2[j - 1].lower():
                lcs_table[i][j] = lcs_table[i - 1][j - 1] + 1
                if lcs_table[i][j] > max_len:
                    max_len = lcs_table[i][j]
                    end_pos = i
            else:
                lcs_table[i][j] = 0

    return str1[end_pos - max_len:end_pos]

def extract_domain_parts(url):
    netloc = urlparse(url).netloc
    domain_parts = netloc.split('.')
    if domain_parts[0].lower() == 'www':
        domain_parts = domain_parts[1:]
    return domain_parts

def match_with_original_company_name(original_name, matched_substr):
    matched_name = []
    matched_index = 0
    original_matched = []
    i = 0

    while i < len(original_name):
        char = original_name[i]
        if re.match(r'[^a-zA-Z0-9]', char):
            original_matched.append(char)
        elif matched_index < len(matched_substr) and char.lower() == matched_substr[matched_index].lower():
            matched_name.append(char)
            original_matched.append(char)
            matched_index += 1
        else:
            original_matched.append(char)
        i += 1

    return ''.join(original_matched)

def check_common_substring(company_names, domain_parts):
    process_result = []  # Logs processing of every word
    all_collections = []  # Stores all matched collections
    longest_collection = ""  # Tracks the longest matched collection

    for domain_part in domain_parts:
        domain_part_lower = domain_part.lower()

        for name in company_names:
            words = name.split()  # Split the company name into words
            current_collection = []  # Temporary collection for matched words

            for i, word in enumerate(words):
                # Check if the current word is a substring of the domain part
                if word.lower() in domain_part_lower:
                    current_collection.append(word)
                    process_result.append({
                        "word": word,
                        "status": "matched",
                        "index": i,
                        "domain_part": domain_part,
                        "current_collection": list(current_collection)
                    })
                else:
                    process_result.append({
                        "word": word,
                        "status": "mismatch",
                        "index": i,
                        "domain_part": domain_part,
                        "reason": "Mismatch found"
                    })

                    if current_collection:
                        collection = " ".join(current_collection)
                        all_collections.append(collection)
                        if len(collection) > len(longest_collection):
                            longest_collection = collection

                        process_result.append({
                            "status": "finalized_collection",
                            "finalized_collection": collection,
                            "reason": "Mismatch triggered finalization"
                        })
                        current_collection = []  # Reset collection

            if current_collection:
                collection = " ".join(current_collection)
                all_collections.append(collection)
                if len(collection) > len(longest_collection):
                    longest_collection = collection

                process_result.append({
                    "status": "end_of_name",
                    "finalized_collection": collection,
                    "reason": "Reached end of company name"
                })

    return {
        "all_collections": all_collections,
        "longest_collection": longest_collection,
        "process_result": process_result
    }

def extract_company_sources(soup):
    sources = {}
    # Get from meta tags
    meta_tag = soup.find('meta', attrs={'property': 'og:site_name'})
    if meta_tag and meta_tag.get('content'):
        sources["meta"] = meta_tag.get('content')

    # Get title tag
    title_tag = soup.find('title')
    if title_tag:
        sources["title_tag"] = title_tag.get_text().strip()

    # Get JSON-LD data if available
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get('@type') == 'Organization':
                if 'name' in data:
                    sources["json_ld"] = data['name']
        except (json.JSONDecodeError, TypeError):
            continue

    # Get image alt text if it contains 'logo'
    for img in soup.find_all('img', alt=True):
        if 'logo' in img['alt'].lower():
            sources["img"] = img['alt'].strip()

    return sources

def main():
    # Check if HTML file argument is provided
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "No HTML file provided. Please provide an HTML file as a command line argument."
        }))
        sys.exit(1)

    pattern = r"Full HTML content saved to html-design(50[0-3]|[1-4]?[0-9]{1,2}|0)\.html$"

    if not re.search(pattern, sys.argv[-1]):
        print(json.dumps({
            "error": "The command must end with 'Full HTML content saved to html-designX.html', where X is between 0-50."
        }))
        sys.exit(1)

    html_file_path = sys.argv[1].strip()
    url = sys.argv[2].strip() if len(sys.argv) > 2 else ""

    # Read HTML content from the specified file
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except FileNotFoundError:
        print(json.dumps({
            "error": f"File not found: {html_file_path}"
        }))
        sys.exit(1)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract emails, phone numbers, social media links, relevant links, company names, and sources
    emails = list(extract_emails(html_content))
    phone_numbers = extract_phone_numbers(soup)
    social_links = extract_social_links(url, soup) if url else {}
    relevant_links = get_relevant_links(url, soup) if url else []
    company_names = extract_company_names(soup)
    sources = extract_company_sources(soup)

    # Extract domain parts from the provided URL
    domain_parts = extract_domain_parts(url) if url else []

    # Check for the common substring in the company names versus domain parts
    matching_results = check_common_substring(company_names, domain_parts) if url else {}
    common_name_part = matching_results.get("longest_collection", "") if url else ""

    # Build the final result (excluding the HTML document)
    result = {
        "emails": emails if emails else "   ",
        "phone_numbers": phone_numbers if phone_numbers else "   ",
        "social_links": social_links,
        "whatsapp_links": social_links.get("whatsapp", []),
        "relevant_links": relevant_links,
        "sources": sources,
        "common_name_part": common_name_part,
        "domain_parts": domain_parts,
        "matching_logs": matching_results.get("process_result", []) if url else []
    }
    # Output the result as a JSON string to the command prompt
    print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
