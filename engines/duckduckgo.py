#!/usr/bin/env python3
# /engines/duckduckgo.py
# Last Updated: 4 feb 2026


from ddgs import DDGS


class DuckDuckGoSearchEngine:

    def __init__(self):
        self.max_results = 10
        self.results = []

    def duckduckgo_api_search(self, query):
        resp = DDGS().text(query, max_results=self.max_results)

        for r in resp:
            self.results.append({"title":    r.get('title', ''),
                            'link':     r.get('href', ''),
                            'desc':  r.get('body', '')
                            })
        return self.results


def ddg_search(query):
    ddgse = DuckDuckGoSearchEngine()
    return ddgse.duckduckgo_api_search(query=query)


if __name__ == "__main__":
    results = ddg_search("SudoHopeX project")
    for result in results:
        print(f"Title: {result['title']}\nLink: {result['link']}\nDescription: {result['desc']}\n")