"""
Web Scrape Tool - Extract content from web pages.

Uses httpx for requests and BeautifulSoup for HTML parsing.
Returns clean text content from web pages.
Respect robots.txt by default for ethical scraping.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup
from fastmcp import FastMCP

# Cache for robots.txt parsers (domain -> parser)
_robots_cache: dict[str, RobotFileParser | None] = {}

# User-Agent for the scraper - identifies as a bot for transparency
USER_AGENT = "AdenBot/1.0 (https://adenhq.com; web scraping tool)"

# Browser-like User-Agent for actual page requests
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def _get_robots_parser(base_url: str, timeout: float = 10.0) -> RobotFileParser | None:
    if base_url in _robots_cache:
        return _robots_cache[base_url]
    robots_url = f"{base_url}/robots.txt"
    parser = RobotFileParser()
    try:
        response = httpx.get(
            robots_url, headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=timeout
        )
        if response.status_code == 200:
            parser.parse(response.text.splitlines())
            _robots_cache[base_url] = parser
            return parser
        else:
            _robots_cache[base_url] = None
            return None
    except (httpx.TimeoutException, httpx.RequestError):
        return None


def _is_allowed_by_robots(url: str) -> tuple[bool, str]:
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    path = parsed.path or "/"
    parser = _get_robots_parser(base_url)
    if parser is None:
        return True, "No robots.txt found or not accessible"
    if parser.can_fetch(USER_AGENT, path) and parser.can_fetch("*", path):
        return True, "Allowed by robots.txt"
    else:
        return False, f"Blocked by robots.txt for path: {path}"


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def web_scrape(
        url: str,
        selector: str | None = None,
        include_links: bool = False,
        max_length: int = 50000,
        respect_robots_txt: bool = True,
    ) -> dict:
        try:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            if respect_robots_txt:
                allowed, reason = _is_allowed_by_robots(url)
                if not allowed:
                    return {
                        "error": f"Scraping blocked: {reason}",
                        "blocked_by_robots_txt": True,
                        "url": url,
                    }
            max_length = max(1000, min(max_length, 500000))
            response = httpx.get(
                url,
                headers={
                    "User-Agent": BROWSER_USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                },
                follow_redirects=True,
                timeout=30.0,
            )
            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}: Failed to fetch URL"}
            content_type_raw = response.headers.get("content-type", "")
            content_type = content_type_raw.lower() if isinstance(content_type_raw, str) else ""
            if not content_type:
                alt = response.headers.get("Content-Type", "")
                content_type = alt.lower() if isinstance(alt, str) else ""
            if not any(t in content_type for t in ["text/html", "application/xhtml+xml"]):
                body_snippet = (response.text or "")[:500].lower()
                if not (
                    "<html" in body_snippet
                    or "<!doctype html" in body_snippet
                    or "<body" in body_snippet
                ):
                    return {
                        "error": f"Skipping non-HTML content (Content-Type: {content_type_raw})",
                        "url": url,
                        "skipped": True,
                    }
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(
                ["script", "style", "nav", "footer", "header", "aside", "noscript", "iframe"]
            ):
                tag.decompose()
            title = soup.title.get_text(strip=True) if soup.title else ""
            description = ""
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc:
                description = meta_desc.get("content", "")
            if selector:
                content_elem = soup.select_one(selector)
                if not content_elem:
                    return {"error": f"No elements found matching selector: {selector}"}
                text = content_elem.get_text(separator=" ", strip=True)
            else:
                main_content = (
                    soup.find("article")
                    or soup.find("main")
                    or soup.find(attrs={"role": "main"})
                    or soup.find(class_=["content", "post", "entry", "article-body"])
                    or soup.find("body")
                )
                text = main_content.get_text(separator=" ", strip=True) if main_content else ""
            text = " ".join(text.split())
            if len(text) > max_length:
                text = text[:max_length] + "..."
            result: dict[str, Any] = {
                "url": str(response.url),
                "title": title,
                "description": description,
                "content": text,
                "length": len(text),
                "robots_txt_respected": respect_robots_txt,
            }
            if include_links:
                links: list[dict[str, str]] = []
                base_url = str(response.url)
                for a in soup.find_all("a", href=True)[:50]:
                    href = a["href"]
                    absolute_href = urljoin(base_url, href)
                    link_text = a.get_text(strip=True)
                    if link_text and absolute_href:
                        links.append({"text": link_text, "href": absolute_href})
                result["links"] = links
            return result
        except httpx.TimeoutException:
            return {"error": "Request timed out"}
        except httpx.RequestError as e:
            return {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"error": f"Scraping failed: {str(e)}"}
