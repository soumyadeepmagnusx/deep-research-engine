"""Researcher Agent:
Executes search queries, crawls relevant web content, and aggregates verified evidence.
"""

from typing import List, Dict, Any
from core.search_tools import live_web_search, extract_web_content


class ResearcherAgent:
    def __init__(self):
        pass

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Search the web for a specific query and extract content."""
        search_results = live_web_search(query, max_results=3)
        evidences = []

        for item in search_results:
            title = item.get("title", "Untitled Source")
            url = item.get("url", "")
            snippet = item.get("snippet", "")

            # Attempt deeper crawl for high-value URLs if valid http
            page_text = ""
            if url.startswith("http"):
                page_text = extract_web_content(url, max_chars=800)

            evidences.append({
                "query": query,
                "title": title,
                "url": url,
                "snippet": snippet,
                "content": page_text or snippet
            })

        return evidences
