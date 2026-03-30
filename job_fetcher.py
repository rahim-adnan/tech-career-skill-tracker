# job_fetcher.py
import time
import requests
from bs4 import BeautifulSoup

class JobFetcher:
    """
    Fetches real job postings from free sources.
    Currently supports:
      - RemoteOK API  (JSON, no key needed)
      - We Work Remotely RSS feed (XML)

    Usage:
        fetcher = JobFetcher(keywords=["python", "machine learning"])
        jobs = fetcher.fetch_all()
        fetcher.show_summary()
    """

    REMOTEOK_URL = "https://remoteok.com/api"
    WWR_RSS_URL  = "https://weworkremotely.com/remote-jobs.rss"

    def __init__(self, keywords: list):
        """
        keywords: list of skills from your CV (output of Step 1)
        """
        self.keywords = [kw.lower() for kw in keywords]
        self.jobs = []   # list of dicts: {title, company, description, source}

    # ── Source 1: RemoteOK ────────────────────────────────────────────────────
    def fetch_remoteok(self) -> list:
        """
        Calls RemoteOK's free public API.
        Returns jobs relevant to your skill keywords.
        """
        print("🌐 Fetching jobs from RemoteOK...")

        headers = {"User-Agent": "Mozilla/5.0 (SkillTracker/1.0)"}

        try:
            response = requests.get(self.REMOTEOK_URL, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # First item is a legal notice, skip it
            job_list = data[1:] if isinstance(data[0], dict) and "legal" in str(data[0]) else data

            found = []
            for job in job_list:
                title       = job.get("position", "").lower()
                tags        = " ".join(job.get("tags", [])).lower()
                description = job.get("description", "").lower()
                combined    = f"{title} {tags} {description}"

                # Only keep jobs that match at least one of your keywords
                if any(kw in combined for kw in self.keywords):
                    found.append({
                        "title"      : job.get("position", "N/A"),
                        "company"    : job.get("company", "N/A"),
                        "description": f"{title} {tags} {description}",
                        "source"     : "RemoteOK",
                        "url"        : job.get("url", ""),
                    })

            print(f"  ✓ RemoteOK: {len(found)} matching jobs found")
            return found

        except requests.exceptions.RequestException as e:
            print(f"  ✗ RemoteOK failed: {e}")
            return []

    # ── Source 2: We Work Remotely RSS ────────────────────────────────────────
    def fetch_weworkremotely(self) -> list:
        """
        Parses the We Work Remotely RSS feed (free, no API key).
        """
        print("🌐 Fetching jobs from We Work Remotely...")

        headers = {"User-Agent": "Mozilla/5.0 (SkillTracker/1.0)"}

        try:
            response = requests.get(self.WWR_RSS_URL, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")

            found = []
            for item in items:
                title       = item.find("title").get_text(strip=True).lower()
                description = item.find("description").get_text(strip=True).lower()
                combined    = f"{title} {description}"

                if any(kw in combined for kw in self.keywords):
                    found.append({
                        "title"      : item.find("title").get_text(strip=True),
                        "company"    : "See listing",
                        "description": combined,
                        "source"     : "WeWorkRemotely",
                        "url"        : item.find("link").get_text(strip=True) if item.find("link") else "",
                    })

            print(f"  ✓ WeWorkRemotely: {len(found)} matching jobs found")
            return found

        except Exception as e:
            print(f"  ✗ WeWorkRemotely failed: {e}")
            return []

    # ── Fetch from all sources ────────────────────────────────────────────────
    def fetch_all(self) -> list:
        """
        Runs all sources and combines results.
        Adds a small delay between requests to be polite.
        """
        print("\n📡 Starting job fetch...\n")

        self.jobs += self.fetch_remoteok()
        time.sleep(1)   # be polite, don't hammer servers
        self.jobs += self.fetch_weworkremotely()

        print(f"\n  ✅ Total jobs collected: {len(self.jobs)}")
        return self.jobs

    # ── Pretty summary ────────────────────────────────────────────────────────
    def show_summary(self):
        """Prints first 5 jobs so you can sanity-check the data."""
        if not self.jobs:
            print("No jobs fetched yet. Run fetch_all() first.")
            return

        print("\n📋 Sample jobs fetched:")
        print("─" * 50)
        for job in self.jobs[:5]:
            print(f"  Title  : {job['title']}")
            print(f"  Company: {job['company']}")
            print(f"  Source : {job['source']}")
            print()
        print("─" * 50)
        print(f"  Total: {len(self.jobs)} jobs ready for skill extraction\n")