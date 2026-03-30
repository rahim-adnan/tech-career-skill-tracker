# skill_extractor.py
from collections import Counter
from cv_parser import SKILL_KEYWORDS   # reuse the same keyword list from Step 1
import re

class SkillExtractor:
    """
    Scans all fetched job descriptions and counts
    how often each skill appears across all jobs.

    Usage:
        extractor = SkillExtractor(jobs)
        extractor.extract()
        extractor.show_top_skills(20)
    """

    def __init__(self, jobs: list):
        """
        jobs: list of job dicts from JobFetcher.fetch_all()
              each dict has at least a 'description' key
        """
        self.jobs = jobs
        self.skill_counts = Counter()    # skill → how many jobs mention it
        self.skill_per_job = []          # list of sets, one per job

    # ── Core extraction ───────────────────────────────────────────────────────
    def extract(self):
        """
        Goes through every job description and counts
        how many jobs mention each skill.
        """
        print(f"\n🔍 Scanning {len(self.jobs)} job descriptions for skills...\n")

        for job in self.jobs:
            description = job.get("description", "").lower()
            description = self._clean(description)

            # Find which skills appear in this single job
            skills_in_this_job = set()
            for skill in SKILL_KEYWORDS:
                pattern = r"\b" + re.escape(skill) + r"\b"
                if re.search(pattern, description):
                    skills_in_this_job.add(skill)

            # Count each skill once per job (not per mention)
            # This gives "X out of 53 jobs need this skill"
            for skill in skills_in_this_job:
                self.skill_counts[skill] += 1

            self.skill_per_job.append(skills_in_this_job)

        print(f"  ✓ Unique skills found across all jobs: {len(self.skill_counts)}")
        return self.skill_counts

    # ── Clean text ────────────────────────────────────────────────────────────
    def _clean(self, text: str) -> str:
        """Remove HTML tags and normalize whitespace."""
        text = re.sub(r"<[^>]+>", " ", text)      # strip HTML tags
        text = re.sub(r"[^\w\s\.\/\+\#]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    # ── Results ───────────────────────────────────────────────────────────────
    def get_top_skills(self, n: int = 20) -> list:
        """
        Returns the top N skills as a list of (skill, count) tuples.
        Sorted from most to least in-demand.
        """
        return self.skill_counts.most_common(n)

    def show_top_skills(self, n: int = 20):
        """Prints a ranked table of the most in-demand skills."""
        top = self.get_top_skills(n)

        if not top:
            print("No skills found. Run extract() first.")
            return

        total_jobs = len(self.jobs)
        print(f"\n🏆 Top {n} In-Demand Skills (from {total_jobs} jobs):")
        print("─" * 55)
        print(f"  {'Rank':<5} {'Skill':<25} {'Jobs':<8} {'% of Jobs'}")
        print("─" * 55)

        for rank, (skill, count) in enumerate(top, 1):
            pct = (count / total_jobs) * 100
            bar = "█" * int(pct / 5)   # simple text bar
            print(f"  {rank:<5} {skill:<25} {count:<8} {pct:>5.1f}%  {bar}")

        print("─" * 55)

    def get_counts_dict(self) -> dict:
        """Returns raw {skill: count} dict — used in Step 4 and Step 5."""
        return dict(self.skill_counts)