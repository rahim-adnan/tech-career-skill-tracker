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
- [ ] Add Netherlands specific job sources
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