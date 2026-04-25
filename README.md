# 🎯 Tech Career Skill Tracker

A web app that reads your CV, fetches live job postings, and shows you exactly which skills are in demand — and which ones you are missing.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

---

## 🚀 Live Demo

[👉 Click here to try it live](https://tech-career-skill-tracker.onrender.com)

---

## 🚀 What It Does

1. **Upload your CV** — supports `.pdf` and `.txt` formats
2. **Detects your skills** — scans for 60+ tech keywords automatically
3. **Fetches live job postings** — pulls from RemoteOK and WeWorkRemotely (free, no API key needed)
4. **Extracts in-demand skills** — scans all job descriptions and counts skill frequency
5. **Gap analysis** — shows which skills you have vs what the job market wants

---

## 📁 Project Structure

```
Tech Career Skill Tracker/
├── app.py                # Streamlit web app — main entry point
├── cv_parser.py          # Step 1 — reads CV and detects your skills
├── job_fetcher.py        # Step 2 — fetches live jobs from free sources
├── skill_extractor.py    # Step 3 — extracts and counts skills from job descriptions
├── visualizer.py         # Step 4 — gap analysis and data processing
├── requirements.txt      # all dependencies
├── setup.sh              # Render server configuration
├── Procfile              # Render start command
├── .gitignore            # files excluded from GitHub
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/rahim-adnan/tech-career-skill-tracker.git
cd tech-career-skill-tracker
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `Streamlit` | Web interface |
| `pdfminer.six` | Extract text from PDF CV files |
| `spaCy` | NLP text processing |
| `requests` | Fetch job postings from APIs and RSS feeds |
| `BeautifulSoup4` + `lxml` | Parse RSS XML feeds |
| `pandas` | Data processing and analysis |

---

## 🌐 Job Sources

| Source | Type | Cost |
|---|---|---|
| [RemoteOK](https://remoteok.com) | JSON API | Free, no key needed |
| [We Work Remotely](https://weworkremotely.com) | RSS Feed | Free, no key needed |

---

## 📈 Possible Upgrades

- [ ] Add more job sources (LinkedIn, Indeed, Adzuna)
- [ ] Schedule weekly runs to track skill trends
- [ ] Auto-generate learning roadmap with free course links
- [ ] Email weekly report automatically

---

## 👤 Author

**Adnan**
- GitHub: [@rahim-adnan](https://github.com/rahim-adnan)

---

## 📄 License

This project is licensed under the MIT License — free to use, modify, and share.