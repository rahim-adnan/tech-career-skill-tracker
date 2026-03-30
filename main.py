# main.py
import os
from cv_parser import CVParser
from job_fetcher import JobFetcher
from skill_extractor import SkillExtractor
from visualizer import SkillVisualizer


def ask_for_cv() -> str:
    """
    Prompts the user to enter their CV file path.
    Keeps asking until a valid .pdf or .txt file is provided.
    """
    print("=" * 50)
    print("  Tech Career Skill Tracker")
    print("=" * 50)
    print("\nSupported formats: .pdf  or  .txt")
    print("Tip: Drag and drop your CV into this terminal.\n")

    while True:
        path = input("Enter the path to your CV file: ").strip()

        # Remove accidental quotes from drag and drop on Windows
        path = path.strip('"').strip("'")

        if not os.path.exists(path):
            print(f"  File not found: {path}")
            print("  Please check the path and try again.\n")
            continue

        if not path.lower().endswith((".pdf", ".txt")):
            print("  Unsupported format. Please use a .pdf or .txt file.\n")
            continue

        print(f"\n  Found: {path}\n")
        return path


def run():
    # ── Step 1: CV Upload and Skill Detection ─────────────────────────────────
    cv_path = ask_for_cv()

    print("Reading your CV...\n")
    parser    = CVParser(cv_path)
    cv_skills = parser.extract_skills()
    parser.show_skills()

    # ── Step 2: Fetch Live Job Postings ───────────────────────────────────────
    fetcher = JobFetcher(keywords=cv_skills)
    jobs    = fetcher.fetch_all()
    fetcher.show_summary()

    # ── Step 3: Extract Skills from Job Descriptions ──────────────────────────
    extractor = SkillExtractor(jobs)
    extractor.extract()
    extractor.show_top_skills(20)

    # ── Steps 4 + 5 + 6: DataFrame, Gap Analysis and Chart ───────────────────
    viz = SkillVisualizer(
        skill_counts = extractor.get_counts_dict(),
        cv_skills    = cv_skills,
        top_n        = 20,
    )
    viz.build_dataframe()
    viz.show_gap_analysis()
    viz.plot()

    # ── Done ──────────────────────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("  All done!")
    print("  skill_trends.png  — bar chart")
    print("  skill_report.csv  — full data table")
    print("=" * 50)


if __name__ == "__main__":
    run()
