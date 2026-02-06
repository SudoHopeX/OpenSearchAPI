"""
Provides Search results for Google Search Engine.
Requires Chrome or Chromium and Xvfb installed on the system.
"""

import nodriver as uc
import asyncio
from pyvirtualdisplay import Display


async def google_search(query):
    # START the Virtual Display here.
    # visible=0 means it runs in the background (hidden)
    # This acts exactly like xvfb-run but inside your code.
    with Display(visible=0, size=(1920, 1080)) as disp:
        # We MUST keep headless=False because nodriver needs to
        # 'see' the virtual display we just created.
        browser = await uc.start(headless=False)

        try:
            page = await browser.get(f"https://www.google.com/search?q={query}&hl=en")

            # Wait for results to stabilize
            await asyncio.sleep(5)

            containers = await page.select_all("div.MjjYud")

            search_results = []
            for container in containers:
                try:
                    title_el = await container.query_selector("h3")
                    link_el = await container.query_selector("a")
                    snippet_el = await container.query_selector("div[style*='-webkit-line-clamp']") or \
                                 await container.query_selector(".VwiC3b")

                    if title_el and link_el:
                        attrs = link_el.attributes
                        link = ""
                        for i in range(len(attrs)):
                            if attrs[i] == "href":
                                link = attrs[i + 1]
                                break

                        if not link or any(x in link for x in ["youtube.com", "youtu.be", "google.com"]):
                            continue

                        search_results.append({
                            "title": title_el.text.strip(),
                            "link": link,
                            "desc": snippet_el.text.replace('\n', ' ').strip() if snippet_el else "No snippet."
                        })
                except Exception:
                    continue

            return search_results

        finally:
            browser.stop()


def run_google_search(query):
    """
    Helper function to run the async google_search in a sync Flask environment.
    """
    return uc.loop().run_until_complete(google_search(query))


if __name__ == "__main__":
    search_results = run_google_search("KaliGPT")
    print(f"\n--- Found {len(search_results)} Clean Organic Results ---")
    for i, res in enumerate(search_results, 1):
        print(f"[{i}] {res['title']}")
        print(f"    URL: {res['link']}")
        print(f"    INFO: {res['desc']}\n")
