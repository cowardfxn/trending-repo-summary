"""
This module fetches the content of a webpage using the requests library and parses
the HTML content using the BeautifulSoup library.
"""

from datetime import datetime
from urllib.parse import urljoin

import markdown
import requests
from bs4 import BeautifulSoup

from git_trendings.parse_intro import distil


def fetch_page(url: str, max_retries: int = 5, timeout: int = 30):
    """
    fetch page content from url. if fetch fails, retry until max_retries
    """
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, timeout=timeout)
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        except requests.exceptions.RequestException as e:
            retries += 1
            print(f"Failed to fetch page {url}, {str(e)}\nRetrying {retries} time(s)")
    print(f"Failed to fetch page {url} after {max_retries} retries")
    return None


def fetch_repo_intro(url: str):
    """
    fetch repo intro from url
    """
    cont = fetch_page(url)
    if cont is None:
        return None

    texts = [l.strip() for l in cont.text.split("\n") if l.strip()]
    return "\n".join(texts)


def fetch_trendings():
    """
    fetch Github daily trending repos
    """
    gihub_base_url = "https://github.com"
    trending_url = f"{gihub_base_url}/trending"
    cont = fetch_page(trending_url)
    if cont is None:
        return []

    ts = cont.find_all("article", attrs={"class": "Box-row"})
    repos = []
    for t in ts:
        if t:
            a = t.find("a", attrs={"data-view-component": "true", "class": "Link"})
            if a:
                title = " ".join([l.strip() for l in a.text.split("\n") if l.strip()])
                href = a.get("href")
                href = urljoin(gihub_base_url, href)
                repos.append((title, href))
    return repos


def trending_repo_intros():
    """
    fetch trending github repos, generate introduction for each repo
    """
    repos = fetch_trendings()
    intros = []
    for title, href in repos:
        intro = fetch_repo_intro(href)
        if intro:
            brief = distil(intro)
            intro = brief if brief else intro
            intros.append((title, href, intro))
    return intros


def gen_report():
    """
    generate trending repos report
    """
    intros = trending_repo_intros()

    # import json

    # with open("./a-output.txt", encoding="utf-8") as ofs:
    #     intros = json.load(ofs)

    if intros:
        blocks = []
        for i, (t, l, c) in enumerate(intros):
            blocks.append(f"## {i+1:02d}. [{t}]({l})\n{c}\n\n")
        # render markdown to html
        html = markdown.markdown("".join(blocks), output_format="html5")
        with open(
            f"./trendings-{datetime.today().strftime('%Y%m%d-%H%M%S')}.html",
            "w",
            encoding="utf-8",
        ) as ofs:
            ofs.write(html)
    else:
        print("Failed to fetch trending repos")


if __name__ == "__main__":
    gen_report()
