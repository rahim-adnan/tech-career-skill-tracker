import streamlit as st
import tempfile
import os
from cv_parser import CVParser
from job_fetcher import JobFetcher
from skill_extractor import SkillExtractor
from visualizer import SkillVisualizer

# ── Wakeup notice ──────────────────────────────────────────
st.info(
    "⏳ **First load?** This app is hosted on Render's free tier and may have "
    "been sleeping. If anything looks slow, give it 30–60 seconds to wake up. "
    "[▶ Watch demo video](YOUR_YOUTUBE_LINK_HERE) while you wait!"
)
# ───────────────────────────────────────────────────────────

st.title("🎯 Tech Career Skill Tracker")
st.write("Upload your CV and see which skills employers want!")

uploaded_file = st.file_uploader("Upload your CV", type=["pdf", "txt"])

if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name}")

    # Step 1 — Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Step 2 — Extract CV skills
    parser    = CVParser(tmp_path)
    cv_skills = parser.extract_skills()

    st.subheader("📄 Skills found in your CV:")
    st.write(cv_skills)

    # Step 3 — Fetch live jobs
    if cv_skills:
        st.subheader("📡 Fetching live jobs...")
        fetcher = JobFetcher(keywords=cv_skills)
        jobs    = fetcher.fetch_all()
        st.success(f"✅ Found {len(jobs)} matching jobs!")

        # Step 4 — Extract skills from jobs
        st.subheader("🔍 Analyzing job market...")
        extractor = SkillExtractor(jobs)
        extractor.extract()
        skill_counts = extractor.get_counts_dict()
        st.success(f"✅ Found {len(skill_counts)} in-demand skills!")

        # Step 5 — Gap Analysis
        st.subheader("📊 Gap Analysis")

        viz = SkillVisualizer(
            skill_counts=skill_counts,
            cv_skills=cv_skills,
            top_n=20,
        )

        df = viz.build_dataframe()

        # Skills you HAVE
        have = df[df["is_gap"] == False]
        missing = df[df["is_gap"] == True]

        st.success(f"✅ Skills you HAVE that employers want ({len(have)}):")
        st.dataframe(have[["skill", "job_count", "percentage"]])

        st.error(f"❌ Skills you are MISSING ({len(missing)}):")
        st.dataframe(missing[["skill", "job_count", "percentage"]])