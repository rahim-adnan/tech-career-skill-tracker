# visualizer.py
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns


class SkillVisualizer:
    """
    Steps 4, 5 and 6 combined:
      - Step 4: Build a ranked DataFrame of skill frequencies
      - Step 5: Gap analysis — highlight skills NOT in your CV
      - Step 6: Plot a color-coded bar chart + save CSV report

    Usage:
        viz = SkillVisualizer(skill_counts, cv_skills)
        viz.build_dataframe()
        viz.show_gap_analysis()
        viz.plot()
    """

    def __init__(self, skill_counts: dict, cv_skills: list, top_n: int = 20):
        """
        skill_counts : dict {skill: count} from SkillExtractor
        cv_skills    : list of skills found in your CV from CVParser
        top_n        : how many top skills to show in the chart
        """
        self.skill_counts = skill_counts
        self.cv_skills    = [s.lower() for s in cv_skills]
        self.top_n        = top_n
        self.df           = None

    # ── Step 4: Build DataFrame ───────────────────────────────────────────────
    def build_dataframe(self) -> pd.DataFrame:
        """
        Converts raw skill counts into a sorted pandas DataFrame.
        Adds columns for percentage and gap status.
        """
        total_jobs = sum(self.skill_counts.values())

        rows = []
        for skill, count in self.skill_counts.items():
            rows.append({
                "skill"      : skill,
                "job_count"  : count,
                "percentage" : round((count / max(total_jobs, 1)) * 100, 1),
                "in_your_cv" : skill.lower() in self.cv_skills,
                "is_gap"     : skill.lower() not in self.cv_skills,
            })

        self.df = (
            pd.DataFrame(rows)
            .sort_values("job_count", ascending=False)
            .head(self.top_n)
            .reset_index(drop=True)
        )

        print(f"\n  [OK] DataFrame built: top {len(self.df)} skills")
        return self.df

    # ── Step 5: Gap Analysis ──────────────────────────────────────────────────
    def show_gap_analysis(self):
        """
        Prints two lists:
          [HAVE]    Skills you already have (in CV + in demand)
          [MISSING] Skills you are missing (in demand but NOT in CV)
        """
        if self.df is None:
            self.build_dataframe()

        have    = self.df[self.df["is_gap"] == False]
        missing = self.df[self.df["is_gap"] == True]

        print("\n" + "=" * 55)
        print("  GAP ANALYSIS — Your CV vs Job Market")
        print("=" * 55)

        print(f"\n  [HAVE] Skills you have that employers want ({len(have)}):")
        print("  " + "-" * 45)
        for _, row in have.iterrows():
            print(f"    + {row['skill']:<25} {row['job_count']} jobs  ({row['percentage']}%)")

        print(f"\n  [MISSING] Skills to learn ({len(missing)}):")
        print("  " + "-" * 45)
        for _, row in missing.iterrows():
            print(f"    - {row['skill']:<25} {row['job_count']} jobs  ({row['percentage']}%)")

        print("\n" + "=" * 55)
        score = len(have) / max(len(self.df), 1) * 100
        print(f"  Your CV covers {score:.0f}% of top {self.top_n} in-demand skills")
        print("=" * 55)

    # ── Step 6: Bar Chart ─────────────────────────────────────────────────────
    def plot(self):
        """
        Draws a clean horizontal bar chart.
        Green = skill you already have in your CV
        Red   = skill missing from your CV (gap to fill)
        Saves chart as skill_trends.png and data as skill_report.csv
        """
        if self.df is None:
            self.build_dataframe()

        # Font that always works on Windows — no missing glyph warnings
        plt.rcParams["font.family"] = "DejaVu Sans"
        sns.set_style("whitegrid")

        # Color each bar
        colors = [
            "#2ecc71" if not gap else "#e74c3c"
            for gap in self.df["is_gap"]
        ]

        # ── Figure ────────────────────────────────────────────────────────────
        fig, ax = plt.subplots(figsize=(13, 8))

        # Plot bars — reversed so rank 1 is at the top
        bars = ax.barh(
            y        = self.df["skill"][::-1],
            width    = self.df["job_count"][::-1],
            color    = list(reversed(colors)),
            edgecolor= "white",
            height   = 0.65,
        )

        # ── Value labels on each bar ──────────────────────────────────────────
        for bar, (_, row) in zip(bars, self.df[::-1].iterrows()):
            ax.text(
                bar.get_width() + 0.2,
                bar.get_y() + bar.get_height() / 2,
                f"{row['job_count']} jobs  ({row['percentage']}%)",
                va        = "center",
                ha        = "left",
                fontsize  = 9,
                color     = "#444444",
            )

        # ── Legend ────────────────────────────────────────────────────────────
        legend_patches = [
            mpatches.Patch(color="#2ecc71", label="[HAVE] Already in your CV"),
            mpatches.Patch(color="#e74c3c", label="[MISSING] Skills to learn"),
        ]
        ax.legend(handles=legend_patches, loc="lower right", fontsize=10)

        # ── Titles and axes ───────────────────────────────────────────────────
        ax.set_xlabel("Number of Job Postings Mentioning This Skill", fontsize=11)
        ax.set_title(
            f"Top {self.top_n} In-Demand Tech Skills\n"
            f"Green = you have it   |   Red = gap to fill",
            fontsize   = 13,
            fontweight = "bold",
            pad        = 15,
        )
        ax.set_xlim(0, self.df["job_count"].max() * 1.4)
        ax.tick_params(axis="y", labelsize=10)
        ax.tick_params(axis="x", labelsize=9)

        plt.tight_layout()

        # ── Save chart ────────────────────────────────────────────────────────
        plt.savefig("skill_trends.png", dpi=150, bbox_inches="tight")
        print("\n  [SAVED] Chart saved as skill_trends.png")

        # ── Save CSV report ───────────────────────────────────────────────────
        self.df.to_csv("skill_report.csv", index=False)
        print("  [SAVED] Data saved as skill_report.csv")

        plt.show()