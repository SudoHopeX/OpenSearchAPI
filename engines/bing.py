#!/usr/bin/env python3
# /engines/bing.py
# Last Updated: 4 feb 2026


import random
import time
from bs4 import BeautifulSoup
from curl_cffi import requests as cffi_requests


class BingSearchEngine:
    def __init__(self):
        self.base_url = "https://www.bing.com/search"
        self.session = cffi_requests.Session()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]


    def _get_headers(self):
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.bing.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
        }

    def search(self, query, pages=1):
        all_results = []

        for page in range(pages):
            # Bing uses the 'first' parameter for pagination (1, 11, 21...)
            offset = page * 10 + 1
            params = {'q': query, 'first': offset}

            try:
                # Impersonate chrome to bypass TLS fingerprinting
                response = self.session.get(
                    self.base_url,
                    params=params,
                    headers=self._get_headers(),
                    impersonate="chrome120",
                    timeout=15
                )

                if response.status_code != 200:
                    print(f"Failed to fetch page {page}. Status: {response.status_code}")
                    break

                results = self._parse_results(response.text)
                all_results.extend(results)

                # Randomized delay to prevent rate-limiting
                time.sleep(random.uniform(2.0, 5.0))

            except Exception as e:
                print(f"An error occurred: {e}")
                break

        return all_results

    @staticmethod
    def _parse_results(self, html):
        soup = BeautifulSoup(html, "html.parser")
        parsed_results = []

        # Primary container for search results
        for item in soup.select("li.b_algo"):
            title_node = item.select_one("h2 a")
            snippet_node = item.select_one(".b_caption p, .b_algoSlug")

            if title_node and title_node.get("href"):
                link = title_node["href"]
                # Clean up Bing redirect URLs if necessary
                if link.startswith("/ck/"):
                    continue  # Skip internal tracker links

                parsed_results.append({
                    "title": title_node.get_text(strip=True),
                    "link": link,
                    "desc": snippet_node.get_text(strip=True) if snippet_node else "No description available."
                })

        return parsed_results


def bing_search(query):
    bse = BingSearchEngine()
    return bse.search(query, pages=2)


# Example usage
if __name__ == "__main__":
    result = bing_search("SudoHopeX")
    for i, res in enumerate(result, 1):
        print(f"{i}. {res['title']}\n   {res['link']}\n {res['desc']}")