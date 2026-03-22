from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


PUBMED_BASE_URL = "https://pubmed.ncbi.nlm.nih.gov"
DEFAULT_TIMEOUT = 15
DEFAULT_MAX_RESULTS = 8


def _build_session() -> requests.Session:
    retry = Retry(
        total=2,
        connect=2,
        read=2,
        backoff_factor=0.6,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }
    )
    return session


def scrape_pubmed_central(theme, pathology, max_results=DEFAULT_MAX_RESULTS, timeout=DEFAULT_TIMEOUT):
    query = f"{(theme or '').strip()} {(pathology or '').strip()}".strip()
    if not query:
        return []

    search_url = f"{PUBMED_BASE_URL}/?term={quote_plus(query)}"
    session = _build_session()

    try:
        response = session.get(search_url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException:
        session.close()
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    study_cards = soup.find_all("article", class_="full-docsum", limit=max_results)

    studies = []
    for card in study_cards:
        title_tag = card.find("a", class_="docsum-title")
        if title_tag is None:
            continue

        title = title_tag.text.strip()
        href = title_tag.get("href", "").strip()
        if not href:
            continue

        link = f"{PUBMED_BASE_URL}{href}"

        author_tag = card.find("span", class_="docsum-authors")
        authors = author_tag.text.strip() if author_tag else "Autores nao disponiveis"

        details = scrape_study_details(session, link, timeout=timeout)
        studies.append(
            {
                "title": title,
                "authors": authors,
                **details,
                "link": link,
            }
        )

    session.close()
    return studies


def scrape_study_details(session, link, timeout=DEFAULT_TIMEOUT):
    fallback = {
        "np": "Informacao nao disponivel",
        "criteria": "Informacao nao disponivel",
        "conclusion": "Informacao nao disponivel",
    }

    try:
        response = session.get(link, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException:
        return fallback

    soup = BeautifulSoup(response.text, "html.parser")
    conclusion_section = soup.find("div", class_="abstract-content selected")

    if not conclusion_section:
        return fallback

    fallback["conclusion"] = conclusion_section.text.strip()
    return fallback
