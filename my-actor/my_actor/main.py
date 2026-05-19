from __future__ import annotations

from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

from apify import Actor
from crawlee import ConcurrencySettings
from crawlee.crawlers import PlaywrightCrawler, BeautifulSoupCrawler

from .routes import get_all_results, router


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}

        # Parse start URLs
        start_urls: list[str] = [
            entry.get("url", "")
            for entry in actor_input.get("startUrls", [])
            if entry.get("url")
        ]

        if not start_urls:
            Actor.log.error("No startUrls provided. Add at least one URL and re-run.")
            await Actor.exit()
            return

        # Extract configuration parameters
        max_requests_per_start_url: int = actor_input.get("maxRequestsPerStartUrl", 20)
        merge_contacts: bool = actor_input.get("mergeContacts", True)
        max_depth: int | None = actor_input.get("maxDepth")
        max_requests: int | None = actor_input.get("maxRequests")
        same_domain: bool = actor_input.get("sameDomain", True)
        consider_child_frames: bool = actor_input.get("considerChildFrames", True)
        
        # Leads enrichment config
        max_leads: int = actor_input.get("maximumLeadsEnrichmentRecords", 0)
        leads_departments: list[str] = actor_input.get("leadsEnrichmentDepartments", [])
        verify_emails: bool = actor_input.get("verifyLeadsEnrichmentEmails", False)
        
        # Social media enrichment config
        social_media_config: dict = actor_input.get("scrapeSocialMediaProfiles", {
            "facebooks": False,
            "instagrams": False,
            "youtubes": False,
            "tiktoks": False,
            "twitters": False
        })
        
        # Browser configuration
        use_browser: bool = actor_input.get("useBrowser", False)
        wait_until: str = actor_input.get("waitUntil", "domcontentloaded")
        
        # Concurrency and timing
        max_concurrency: int = actor_input.get("max_concurrency", 5)
        nav_timeout_secs: int = actor_input.get("navigation_timeout_secs", 60)

        # Proxy configuration
        proxy_configuration = None
        if proxy_config_input := actor_input.get("proxy_configuration"):
            proxy_configuration = await Actor.create_proxy_configuration(
                actor_proxy_input=proxy_config_input
            )

        # Store configuration globally for use in route handlers
        Actor.config = {
            "start_urls": start_urls,
            "max_requests_per_start_url": max_requests_per_start_url,
            "merge_contacts": merge_contacts,
            "max_depth": max_depth,
            "same_domain": same_domain,
            "consider_child_frames": consider_child_frames,
            "max_leads": max_leads,
            "leads_departments": leads_departments,
            "verify_emails": verify_emails,
            "social_media_config": social_media_config,
            "use_browser": use_browser,
            "wait_until": wait_until,
        }

        # Extract domain from start URLs for same-domain checking
        allowed_domains: set[str] = set()
        for url in start_urls:
            try:
                domain = urlparse(url).netloc
                allowed_domains.add(domain)
            except Exception:
                pass

        Actor.config["allowed_domains"] = allowed_domains

        # Create the appropriate crawler based on configuration
        crawler_config = {
            "max_requests_per_crawl": max_requests,
            "concurrency_settings": ConcurrencySettings(
                max_concurrency=max_concurrency,
                desired_concurrency=max_concurrency,
            ),
            "headless": True,
            "max_request_retries": 3,
            "proxy_configuration": proxy_configuration,
            "request_handler": router,
        }

        if use_browser:
            crawler_config.update({
                "browser_launch_options": {
                    "args": [
                        "--disable-gpu",
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-setuid-sandbox",
                        "--disable-web-security",
                        "--disable-features=IsolateOrigins,site-per-process",
                        "--blink-settings=imagesEnabled=false",
                        "--disable-extensions",
                    ],
                },
                "navigation_timeout": timedelta(seconds=nav_timeout_secs),
                "wait_until": wait_until,
            })
            crawler = PlaywrightCrawler(**crawler_config)
        else:
            # Use BeautifulSoup crawler for faster static scraping
            crawler = BeautifulSoupCrawler(**crawler_config)

        # Enqueue URLs with depth tracking
        for i, url in enumerate(start_urls):
            await crawler.add_requests([
                {
                    "url": url,
                    "userData": {
                        "depth": 0,
                        "originalStartUrl": url,
                        "startUrlIndex": i,
                    }
                }
            ])

        # Run the crawler
        await crawler.run()

        # Collect and push results
        all_results = get_all_results()
        
        for result in all_results:
            await Actor.push_data(result)

        # Push summary
        summary = {
            "type": "SUMMARY",
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "total_results": len(all_results),
            "start_urls": start_urls,
            "merge_contacts_enabled": merge_contacts,
        }
        
        await Actor.push_data(summary)
        await Actor.set_value("OUTPUT", summary)