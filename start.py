from dotenv import load_dotenv

from git_trendings.afetcher import agen_report

load_dotenv(override=True)

if __name__ == "__main__":
    agen_report()
