# cv_parser.py

import re
from pathlib import Path
from pdfminer.high_level import extract_text  # reads PDF files
import spacy

# ── Predefined skill dictionary ──────────────────────
SKILL_KEYWORDS = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "kotlin", "swift", "r", "scala", "sql",

    # AI / ML
    "machine learning", "deep learning", "neural network", "nlp",
    "natural language processing", "computer vision", "reinforcement learning",
    "tensorflow", "pytorch", "keras", "scikit-learn", "hugging face",
    "transformers", "llm", "large language model",

    # Data Science
    "pandas", "numpy", "matplotlib", "seaborn", "tableau", "power bi",
    "data analysis", "data visualization", "statistics", "spark", "hadoop",

    # Cybersecurity
    "cybersecurity", "penetration testing", "ethical hacking", "nmap", "kali linux",
    "siem", "firewall", "ids", "ips", "encryption", "owasp", "ctf",

    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "terraform" ,
    "linux", "git", "github", "jenkins",

    # Web / General
    "django", "flask", "fastapi", "react", "node.js", "rest api", "graphql",
    "mongodb", "postgresql", "redis",
]


class CVParser:
    """
    Reads a CV (PDF or .txt) and extracts skills from it.

    Usage:
        parser = CVParser("my_cv.pdf")
        skills = parser.extract_skills()
        print(skills)
    """

    def __init__(self, filepath: str):
        """
        filepath: path to your CV file (PDF or .txt)
        """
        self.filepath = Path(filepath)
        self.raw_text = ""
        self.skills_found = []

        # Load spaCy's English model (used for smarter text cleaning)
        self.nlp = spacy.load("en_core_web_sm")

    # ── Step 1A: Read the file ────────────────────────────────────────────────
    def load_text(self) -> str:
        """Reads the CV file and returns raw text."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {self.filepath}")

        if self.filepath.suffix.lower() == ".pdf":
            self.raw_text = extract_text(str(self.filepath))
        elif self.filepath.suffix.lower() in [".txt", ".md"]:
            self.raw_text = self.filepath.read_text(encoding="utf-8")
        else:
            raise ValueError("Only .pdf and .txt files are supported.")

        print(f"[✓] Loaded CV: {len(self.raw_text)} characters")
        return self.raw_text

    # ── Step 1B: Clean the text ───────────────────────────────────────────────
    def clean_text(self, text: str) -> str:
        """Lowercase + remove special chars, keep letters/numbers/spaces."""
        text = text.lower()
        text = re.sub(r"[^\w\s\.\/\+\#]", " ", text)  # keep c++, c#, etc.
        text = re.sub(r"\s+", " ", text)  # collapse whitespace
        return text.strip()

    # ── Step 1C: Match skills ─────────────────────────────────────────────────
    def extract_skills(self) -> list:
        """
        Main method — runs the full pipeline:
        load → clean → match against SKILL_KEYWORDS → return list of found skills
        """
        if not self.raw_text:
            self.load_text()

        cleaned = self.clean_text(self.raw_text)

        found = []
        for skill in SKILL_KEYWORDS:
            # Use word-boundary matching so "r" doesn't match inside "architecture"
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, cleaned):
                found.append(skill)

        self.skills_found = found
        print(f"[✓] Skills detected in your CV: {len(found)}")
        return found

    # ── Utility: pretty print ─────────────────────────────────────────────────
    def show_skills(self):
        """Prints your detected skills in a readable way."""
        if not self.skills_found:
            print("Run extract_skills() first.")
            return
        print("\n📄 Skills found in your CV:")
        print("─" * 40)
        for i, skill in enumerate(self.skills_found, 1):
            print(f"  {i:>2}. {skill}")
        print("─" * 40)
        print(f"  Total: {len(self.skills_found)} skills\n")