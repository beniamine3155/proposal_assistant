import trafilatura

def scrape_website(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)

    if not downloaded:
        raise ValueError("Failed to fetch website")

    text = trafilatura.extract(
        downloaded,
        include_tables=True,
        include_comments=False
    )

    if not text:
        raise ValueError("No readable content found")

    return text
