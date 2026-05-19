"""Comprehensive contact extraction logic for Contact Details Scraper Actor."""

from __future__ import annotations

import asyncio
import re
import urllib.parse
from typing import Set, Dict, Any
from urllib.parse import urlparse

from apify import Actor
from crawlee.crawlers import PlaywrightCrawlingContext, BeautifulSoupCrawlingContext
from crawlee.router import Router

router = Router()

# Global storage for results per domain
_results_by_domain: Dict[str, Dict[str, Any]] = {}
_urls_by_domain: Dict[str, Set[str]] = {}


def get_all_results() -> list[dict]:
    """Return all results collected across all domains."""
    results = list(_results_by_domain.values())
    return results


# ---------------------------------------------------------------------------
# REGEX PATTERNS FOR CONTACT EXTRACTION
# ---------------------------------------------------------------------------

# Email patterns
STRICT_EMAIL_RE = re.compile(
    r'(?<![=\w])'
    r'([a-zA-Z0-9][a-zA-Z0-9._%+\-]{0,63}'
    r'@'
    r'(?:[a-zA-Z0-9\-]{1,63}\.)+[a-zA-Z]{2,24})',
)

OBFUSCATED_EMAIL_RE = re.compile(
    r'([a-zA-Z0-9][a-zA-Z0-9._%+\-]{0,63})'
    r'\s*[\[(]?\s*(?:at|AT|@)\s*[\])]?\s*'
    r'([a-zA-Z0-9\-]{1,63}'
    r'(?:\s*[\[(]?\s*(?:dot|DOT|\.)\s*[\])]?\s*[a-zA-Z0-9\-]{1,63})+)'
    r'\s*[\[(]?\s*(?:dot|DOT|\.)\s*[\])]?\s*'
    r'([a-zA-Z]{2,24})',
)

# Phone number patterns (various formats)
PHONE_RE = re.compile(
    r'(?:(?:\+|0{1,2})\s*)?'  # Optional country code
    r'(?:\(?\d{1,3}\)?[\s.-]?)?'  # Area code
    r'(?:\d{1,4}[\s.-]?){2}\d{1,4}',  # Rest of number
)

# Social media URLs
LINKEDIN_RE = re.compile(r'https?://(?:www\.)?linkedin\.com/\S+', re.IGNORECASE)
TWITTER_RE = re.compile(r'https?://(?:www\.|m\.)?(?:twitter\.com|x\.com)/\S+', re.IGNORECASE)
INSTAGRAM_RE = re.compile(r'https?://(?:www\.)?instagram\.com/\S+', re.IGNORECASE)
FACEBOOK_RE = re.compile(r'https?://(?:www\.)?facebook\.com/\S+', re.IGNORECASE)
YOUTUBE_RE = re.compile(r'https?://(?:www\.)?youtube\.com/\S+|https?://youtu\.be/\S+', re.IGNORECASE)
TIKTOK_RE = re.compile(r'https?://(?:www\.)?tiktok\.com/@\S+|https?://vm\.tiktok\.com/\S+', re.IGNORECASE)
PINTEREST_RE = re.compile(r'https?://(?:www\.)?pinterest\.com/\S+', re.IGNORECASE)
DISCORD_RE = re.compile(r'https?://(?:www\.)?discord\.(?:com|gg)/\S+', re.IGNORECASE)
TELEGRAM_RE = re.compile(r'https?://(?:t\.me|telegram\.org)/\S+', re.IGNORECASE)
REDDIT_RE = re.compile(r'https?://(?:www\.)?reddit\.com/(?:r|u)/\S+', re.IGNORECASE)
SNAPCHAT_RE = re.compile(r'https?://(?:www\.)?snapchat\.com/\S+', re.IGNORECASE)
THREADS_RE = re.compile(r'https?://(?:www\.)?threads\.net/@\S+', re.IGNORECASE)
WHATSAPP_RE = re.compile(r'(?:https?://)?(?:wa\.me|whatsapp\.com)/\S+', re.IGNORECASE)

# Rejection lists
REJECT_TLDS = {
    'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'ico', 'css', 'js', 'json',
    'xml', 'pdf', 'zip', 'tar', 'gz', 'mp4', 'mp3', 'wav', 'woff', 'woff2',
    'ttf', 'eot', 'map', 'ts', 'tsx', 'jsx', 'vue', 'scss', 'sass', 'less',
}
REJECT_LOCALS = {
    'example', 'test', 'noreply', 'no-reply', 'donotreply', 'do-not-reply',
    'webmaster', 'postmaster', 'mailer-daemon', 'mailer_daemon', 'bounce',
    'bounces', 'null', 'nobody', 'devnull', 'dev-null', 'spam', 'nospam',
}
REJECT_DOMAINS = {
    'example.com', 'example.org', 'example.net', 'test.com', 'test.org',
    'localhost.com', 'sentry.io', 'sentry-cdn.com', 'schema.org',
    'w3.org', 'w3c.org', 'googletagmanager.com', 'google-analytics.com',
}


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def _decode_obfuscations(text: str) -> str:
    """Replace common encoding tricks with plain characters."""
    text = re.sub(r'&#(?:64|x40);', '@', text, flags=re.IGNORECASE)
    text = re.sub(r'\\u0040', '@', text, flags=re.IGNORECASE)
    return text.replace('%40', '@')


def _extract_from_mailto(html: str) -> Set[str]:
    """Pull emails from href="mailto:…"."""
    emails: Set[str] = set()
    for m in re.finditer(r'href=["\']mailto:([^"\'?\s>]+)', html, re.IGNORECASE):
        raw = urllib.parse.unquote(m.group(1))
        for candidate in raw.split(','):
            candidate = candidate.strip()
            if '@' in candidate:
                emails.add(candidate.lower())
    return emails


def _extract_standard_emails(text: str) -> Set[str]:
    """Extract standard email format."""
    return {m.group(1).lower() for m in STRICT_EMAIL_RE.finditer(text)}


def _extract_obfuscated_emails(text: str) -> Set[str]:
    """Extract obfuscated emails like name [at] domain [dot] com."""
    emails: Set[str] = set()
    for m in OBFUSCATED_EMAIL_RE.finditer(text):
        middle = re.sub(r'\s*[\[(]?\s*(?:dot|DOT|\.)\s*[\])]?\s*', '.', m.group(2)).strip('.')
        emails.add(f'{m.group(1).strip()}@{middle}.{m.group(3).strip()}'.lower())
    return emails


def _filter_emails(emails: Set[str]) -> Set[str]:
    """Remove false positives from email set."""
    clean: Set[str] = set()
    for email in emails:
        email = email.strip().strip('.')
        if '@' not in email:
            continue
        local, _, domain = email.partition('@')
        if '.' not in domain:
            continue
        tld = domain.rsplit('.', 1)[-1].lower()
        if tld in REJECT_TLDS or local.lower() in REJECT_LOCALS or domain.lower() in REJECT_DOMAINS:
            continue
        if len(local) < 1 or len(domain) < 4 or '..' in local:
            continue
        clean.add(email)
    return clean


def extract_all_emails(html: str, visible_text: str, shadow_text: str = '') -> Set[str]:
    """Run all email extraction strategies."""
    src_html = _decode_obfuscations(html)
    src_text = _decode_obfuscations(visible_text)
    src_shadow = _decode_obfuscations(shadow_text)

    found: Set[str] = set()
    found.update(_extract_from_mailto(src_html))
    found.update(_extract_standard_emails(src_html))
    found.update(_extract_standard_emails(src_text))
    found.update(_extract_standard_emails(src_shadow))
    found.update(_extract_obfuscated_emails(src_html))
    found.update(_extract_obfuscated_emails(src_text))
    
    return _filter_emails(found)


def extract_phones(text: str) -> tuple[Set[str], Set[str]]:
    """Extract phone numbers. Returns (verified, uncertain)."""
    phones: Set[str] = set()
    uncertain: Set[str] = set()
    
    for match in PHONE_RE.finditer(text):
        phone = match.group(0).strip()
        # Clean up
        phone = re.sub(r'\s+', '', phone)
        if len(phone) >= 7:  # Reasonable minimum
            # Heuristic: if looks like international format, likely verified
            if phone.startswith(('+', '00')) or re.match(r'^\+?\d{10,}$', phone):
                phones.add(phone)
            else:
                uncertain.add(phone)
    
    return phones, uncertain


def extract_social_media(html: str, text: str) -> Dict[str, Set[str]]:
    """Extract all social media URLs."""
    combined = f"{html} {text}".lower()
    
    return {
        "linkedIns": set(m.group(0) for m in LINKEDIN_RE.finditer(combined)),
        "twitters": set(m.group(0) for m in TWITTER_RE.finditer(combined)),
        "instagrams": set(m.group(0) for m in INSTAGRAM_RE.finditer(combined)),
        "facebooks": set(m.group(0) for m in FACEBOOK_RE.finditer(combined)),
        "youtubes": set(m.group(0) for m in YOUTUBE_RE.finditer(combined)),
        "tiktoks": set(m.group(0) for m in TIKTOK_RE.finditer(combined)),
        "pinterests": set(m.group(0) for m in PINTEREST_RE.finditer(combined)),
        "discords": set(m.group(0) for m in DISCORD_RE.finditer(combined)),
        "telegrams": set(m.group(0) for m in TELEGRAM_RE.finditer(combined)),
        "reddits": set(m.group(0) for m in REDDIT_RE.finditer(combined)),
        "snapchats": set(m.group(0) for m in SNAPCHAT_RE.finditer(combined)),
        "threads": set(m.group(0) for m in THREADS_RE.finditer(combined)),
        "whatsapps": set(m.group(0) for m in WHATSAPP_RE.finditer(combined)),
    }


def get_domain(url: str) -> str:
    """Extract domain from URL."""
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


async def _scroll_to_load_lazy(context) -> None:
    """Scroll incrementally to trigger lazy-loaded sections."""
    try:
        if hasattr(context, 'page'):
            await context.page.evaluate(
                """async () => {
                    const delay = ms => new Promise(r => setTimeout(r, ms));
                    let last = 0;
                    for (let i = 0; i < 10; i++) {
                        window.scrollTo(0, document.body.scrollHeight);
                        await delay(400);
                        if (document.body.scrollHeight === last) break;
                        last = document.body.scrollHeight;
                    }
                    window.scrollTo(0, 0);
                }"""
            )
    except Exception:
        pass


async def _expand_hidden_sections(context) -> None:
    """Click accordions, tabs, and 'show more' elements."""
    if not hasattr(context, 'page'):
        return
    
    selectors = [
        '[data-toggle="collapse"]',
        '[aria-expanded="false"]',
        '.accordion-button',
        '[role="tab"]:not([aria-selected="true"])',
        'button:has-text("Show more")',
        'button:has-text("Contact")',
        'a:has-text("Contact us")',
        '[class*="expand"]',
        '[class*="toggle"]',
    ]
    
    for selector in selectors:
        try:
            for el in (await context.page.locator(selector).all())[:5]:
                try:
                    await el.click(timeout=1500)
                    await asyncio.sleep(0.2)
                except Exception:
                    pass
        except Exception:
            pass


async def _get_shadow_dom_text(context) -> str:
    """Recursively collect text from shadow roots."""
    if not hasattr(context, 'page'):
        return ''
    
    try:
        return await context.page.evaluate(
            """() => {
                const texts = [];
                function walk(root) {
                    root.querySelectorAll('*').forEach(el => {
                        if (el.shadowRoot) walk(el.shadowRoot);
                        if (el.textContent) texts.push(el.textContent);
                    });
                }
                walk(document);
                return texts.join(' ');
            }"""
        )
    except Exception:
        return ''


# ---------------------------------------------------------------------------
# ROUTE HANDLERS
# ---------------------------------------------------------------------------

@router.default_handler
async def default_handler(context) -> None:
    """
    Main handler for scraping pages and extracting contact information.
    """
    url = context.request.url
    user_data = context.request.user_data or {}
    depth = user_data.get("depth", 0)
    original_start_url = user_data.get("originalStartUrl", url)
    
    Actor.log.info(f'Scraping: {url} (depth: {depth})')
    
    try:
        # Get configuration
        config = getattr(Actor, 'config', {})
        max_depth = config.get('max_depth')
        same_domain = config.get('same_domain', True)
        consider_child_frames = config.get('consider_child_frames', True)
        
        # Check depth limit
        if max_depth is not None and depth > max_depth:
            Actor.log.info(f'  → Max depth reached, skipping')
            return
        
        # Check domain limit
        domain = get_domain(url)
        original_domain = get_domain(original_start_url)
        
        if same_domain and domain != original_domain:
            Actor.log.info(f'  → Different domain, skipping')
            return
        
        # Get page content
        html = ""
        visible_text = ""
        shadow_text = ""
        
        if hasattr(context, 'page'):
            # Browser-based extraction
            try:
                await context.page.wait_for_load_state('networkidle', timeout=20_000)
            except Exception:
                try:
                    await context.page.wait_for_load_state('domcontentloaded', timeout=10_000)
                except Exception:
                    pass
            
            await _scroll_to_load_lazy(context)
            await _expand_hidden_sections(context)
            await asyncio.sleep(0.5)
            
            try:
                html = await context.page.content()
            except Exception:
                html = ""
            
            try:
                visible_text = await context.page.evaluate(
                    "() => document.body ? document.body.innerText : ''"
                )
            except Exception:
                visible_text = ""
            
            shadow_text = await _get_shadow_dom_text(context)
        else:
            # BeautifulSoup extraction
            try:
                html = await context.http_client.fetch(url)
                visible_text = context.soup.get_text(separator=' ', strip=True) if hasattr(context, 'soup') else ""
            except Exception:
                html = ""
                visible_text = ""
        
        # Extract contacts
        emails = extract_all_emails(html, visible_text, shadow_text)
        phones, phones_uncertain = extract_phones(visible_text + html)
        social_media = extract_social_media(html, visible_text)
        
        # Initialize or update result for this domain
        if original_domain not in _results_by_domain:
            _results_by_domain[original_domain] = {
                "originalStartUrl": original_start_url,
                "domain": original_domain,
                "depth": depth,
                "emails": set(),
                "phones": set(),
                "phonesUncertain": set(),
                "linkedIns": set(),
                "twitters": set(),
                "instagrams": set(),
                "facebooks": set(),
                "youtubes": set(),
                "tiktoks": set(),
                "pinterests": set(),
                "discords": set(),
                "snapchats": set(),
                "threads": set(),
                "telegrams": set(),
                "reddits": set(),
                "whatsapps": set(),
                "facebookProfiles": [],
                "instagramProfiles": [],
                "youtubeProfiles": [],
                "tiktokProfiles": [],
                "twitterProfiles": [],
                "leadsEnrichment": [],
                "scrapedUrls": [],
            }
            _urls_by_domain[original_domain] = set()
        
        result = _results_by_domain[original_domain]
        result["emails"].update(emails)
        result["phones"].update(phones)
        result["phonesUncertain"].update(phones_uncertain)
        
        for key in social_media:
            result[key].update(social_media[key])
        
        _urls_by_domain[original_domain].add(url)
        result["scrapedUrls"] = list(_urls_by_domain[original_domain])
        
        if emails:
            Actor.log.info(f'  → Found {len(emails)} email(s)')
        
        # Enqueue same-domain links if within depth limit
        if max_depth is None or depth < max_depth:
            if hasattr(context, 'enqueue_links'):
                try:
                    await context.enqueue_links(
                        strategy='same-domain' if same_domain else 'all',
                        exclude=[
                            r'.*\.(jpg|jpeg|png|gif|svg|webp|ico|pdf|zip|tar|gz|'
                            r'mp4|mp3|wav|woff|woff2|ttf|eot|css|js|json|xml)(\?.*)?$',
                        ],
                        user_data={
                            "depth": depth + 1,
                            "originalStartUrl": original_start_url,
                        }
                    )
                except Exception as e:
                    Actor.log.warning(f'  → Error enqueueing links: {e}')
    
    except Exception as e:
        Actor.log.error(f'  → Error scraping {url}: {e}')


@router.error_handler
async def error_handler(context) -> None:
    """Handle errors during crawling."""
    Actor.log.error(f'Request failed: {context.request.url}')
