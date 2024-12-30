import asyncio
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup
from git_trendings.parse_intro import adistil, get_adistil_rslt

from utils import atimer


async def afetch_page(
    session: aiohttp.ClientSession, url: str, max_retries: int = 5, timeout: int = 30
):
    """
    fetch page content from url. if fetch fails, retry until max_retries
    """
    retries = 0
    while retries < max_retries:
        try:
            async with session.get(url, timeout=timeout) as response:
                response_text = await response.text()
                soup = BeautifulSoup(response_text, "html.parser")
                return soup
        except aiohttp.ClientError as e:
            retries += 1
            print(f"Failed to fetch page {url}, {str(e)}\nRetrying {retries} time(s)")
    print(f"Failed to fetch page {url} after {max_retries} retries")
    return None


async def afetch_repo_intro(session: aiohttp.ClientSession, url: str):
    """
    fetch repo intro from url
    """
    cont = await afetch_page(session, url)
    if cont is None:
        return None

    texts = [l.strip() for l in cont.text.split("\n") if l.strip()]
    return "\n".join(texts)


@atimer
async def afetch_trendings(session: aiohttp.ClientSession):
    """
    fetch Github daily trending repos
    """
    github_base_url = "https://github.com"
    trending_url = f"{github_base_url}/trending"

    cont = await afetch_page(session, trending_url)
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
                href = urljoin(github_base_url, href)
                repos.append((title, href))
    return repos


@atimer
async def atrending_repo_intros():
    """
    fetch trending github repos, generate introduction for each repo
    """
    intros = []
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(30)) as session:
        repos = await afetch_trendings(session)
        tasks = [afetch_repo_intro(session, href) for _, href in repos]
        intros_results = await asyncio.gather(*tasks)
        rslt_ids = [adistil(intro) for intro in intros_results]
        rslts = get_adistil_rslt(rslt_ids)
        for (title, href), intro in zip(repos, rslts):
            intros.append((title, href, intro))
    return intros


# if __name__ == "__main__":
#     import asyncio, json

#     loop = asyncio.get_event_loop()
#     repos = loop.run_until_complete(atrending_repo_intros())
#     with open("./a-output.txt", "w") as f:
#         json.dump(repos, f, indent=4)
#     print("Done")
