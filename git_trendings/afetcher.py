import asyncio
from datetime import datetime

from markdown import markdown

from git_trendings.async_fetcher import atrending_repo_intros
from git_trendings.parse_intro import adistil

loop = asyncio.get_event_loop()


def agen_report():
    intros = loop.run_until_complete(atrending_repo_intros())

    if intros:
        blocks = []
        for i, (t, l, c) in enumerate(intros):
            blocks.append(f"## {i+1:02d}. [{t}]({l})\n{c}\n\n")
        # render markdown to html
        html = markdown("\n---\n".join(blocks), output_format="html5")
        # embed rendered html into a html file
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GitHub Trending Repositories</title>
        </head>
        <body style="font-family: Arial, sans-serif; max-width: 80%; margin: 2rem auto">
            {html}
        </body>
        </html>
        """
        with open(
            f"./trendings-{datetime.today().strftime('%Y%m%d-%H%M%S')}.html",
            "w",
            encoding="utf-8",
        ) as ofs:
            ofs.write(html)
    else:
        print("Failed to fetch trending repos")
