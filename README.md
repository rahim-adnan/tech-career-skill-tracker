# 🎯 Tech Career Skill Tracker

A Python tool that reads your CV, fetches live job postings, and shows you exactly which skills are in demand — and which ones you are missing.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📸 Output Preview

The tool generates a color-coded bar chart saved as `skill_trends.png`:

- 🟢 **Green bars** — skills you already have in your CV
- 🔴 **Red bars** — skills missing from your CV (gaps to fill)

---

## 🚀 What It Does

1. **Upload your CV** — supports `.pdf` and `.txt` formats
2. **Detects your skills** — scans for 60+ tech keywords automatically
3. **Fetches live job postings** — pulls from RemoteOK and WeWorkRemotely (free, no API key needed)
4. **Extracts in-demand skills** — scans all job descriptions and counts skill frequency
5. **Gap analysis** — compares your CV skills vs what the job market wants
6. **Visualizes trends** — generates a bar chart and saves a CSV report

---

## 📁 Project Structure

```
Tech Career Skill Tracker/
├── cv_parser.py          # Step 1 — reads CV, detects your skills
├── job_fetcher.py        # Step 2 — fetches live jobs from free sources
├── skill_extractor.py    # Step 3 — extracts and counts skills from job descriptions
├── visualizer.py         # Steps 4-6 — gap analysis, bar chart, CSV export
├── main.py               # Entry point — runs the full pipeline
├── .gitignore            # Files excluded from GitHub
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/rahim-adnan/tech-career-skill-tracker.git
cd tech-career-skill-tracker
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install pdfminer.six spacy requests beautifulsoup4 lxml pandas matplotlib seaborn
python -m spacy download en_core_web_sm
```

---

## ▶️ Usage

```bash
python main.py
```

You will be prompted to enter your CV file path:

```
==================================================
  Tech Career Skill Tracker
==================================================

Supported formats: .pdf  or  .txt
Tip: Drag and drop your CV into this terminal.

Enter the path to your CV file: "D:\CV\YourName_CV.pdf"
```

**On Windows:** You can drag and drop your CV file directly into the terminal to get its full path automatically.

---

## 📊 Sample Output

```
[✓] Loaded CV: 2170 characters
[✓] Skills detected in your CV: 9

Skills found in your CV:
────────────────────────────────────────
   1. python
   2. javascript
   3. sql
   4. machine learning
   5. computer vision
   6. pandas
   7. numpy
   8. git
   9. flask
────────────────────────────────────────

Starting job fetch...

  RemoteOK:        53 matching jobs found
  WeWorkRemotely:  45 matching jobs found
  Total jobs:      98

Top 20 In-Demand Skills (from 98 jobs):
───────────────────────────────────────────────────────
  Rank  Skill                     Jobs     % of Jobs
───────────────────────────────────────────────────────
  1     ci/cd                     18        18.4%  ███
  2     python                    18        18.4%  ███
  3     aws                       15        15.3%  ███
  ...

GAP ANALYSIS — Your CV vs Job Market
=======================================================

  [HAVE] Skills you have that employers want (5):
    + python                    18 jobs  (18.4%)
    + javascript                13 jobs  (13.3%)
    + sql                        9 jobs   (9.2%)
    + git                        7 jobs   (7.1%)
    + machine learning           7 jobs   (7.1%)

  [MISSING] Skills to learn (15):
    - ci/cd                     18 jobs  (18.4%)
    - aws                       15 jobs  (15.3%)
    - react                     14 jobs  (14.3%)
    ...

  Your CV covers 25% of top 20 in-demand skills
=======================================================

  [SAVED] Chart  -> skill_trends.png
  [SAVED] Report -> skill_report.csv
```

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `pdfminer.six` | Extract text from PDF CV files |
| `spaCy` | NLP text processing |
| `requests` | Fetch job postings from APIs and RSS feeds |
| `BeautifulSoup4` + `lxml` | Parse RSS XML feeds |
| `pandas` | Build and export skill frequency DataFrames |
| `matplotlib` + `seaborn` | Plot the bar chart |

All libraries are **free and open source**. No API keys required.

---

## 🌐 Job Sources

| Source | Type | Cost |
|---|---|---|
| [RemoteOK](https://remoteok.com) | JSON API | Free, no key needed |
| [We Work Remotely](https://weworkremotely.com) | RSS Feed | Free, no key needed |

---

## 🔧 Customization

### Add more skills to detect

Open `cv_parser.py` and add to the `SKILL_KEYWORDS` list:

```python
SKILL_KEYWORDS = [
    # Add your own here
    "langchain", "openai", "rust", "solidity", "stable diffusion",
]
```

### Change number of top skills shown

In `main.py` adjust `top_n`:

```python
viz = SkillVisualizer(
    skill_counts = extractor.get_counts_dict(),
    cv_skills    = cv_skills,
    top_n        = 30,   # show top 30 instead of 20
)
```

---

## 📈 Possible Upgrades

- [ ] Add more job sources (Remotive, Adzuna, LinkedIn RSS)
- [ ] Schedule weekly runs to track skill trends over time
- [ ] Build a Flask web interface
- [ ] Auto-generate a learning roadmap with free course links
- [ ] Email the weekly report to yourself automatically

---

## 👤 Author

**Adnan**
- GitHub: [@rahim-adnan](https://github.com/rahim-adnan)

---

## 📄 License

This project is licensed under the MIT License — free to use, modify, and share.
