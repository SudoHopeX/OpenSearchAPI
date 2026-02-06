#!/usr/bin/env python3
# /engines/__init__.py
# Last Updated: 4 feb 2026

# engine module for getting engine search results

from .duckduckgo import ddg_search
from .bing import bing_search
from .google import run_google_search as google_search


def search(query, engine):
    """
    Fetching search results from engines

    Args:
        query: search query to fetch results
        engine: engine to use for fetching search results

    Returns:
        returns a list of search results in the form
                    [
                    {"title": "title", "link": "link", "desc": "desc"},
                    {....},
                    ,,,
                    ]
    """

    match engine:
        case "google":
            return google_search(query=query)

        case "bing":
            return bing_search(query=query)

        case "duckduckgo":
            return ddg_search(query=query)

        case _:
            return "Engine Not Supported"



if __name__ == "__main__":
    print(search("hello", "bing"))