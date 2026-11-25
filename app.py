"""
AI-Powered Resume Analyzer and Career Assistant Using Generative AI and LLMs.
Streamlit Main Application Dashboard.
"""
import streamlit as st
from config import GEMINI_API_KEY, MAX_UPLOAD_SIZE_MB
from modules.pdf_extractor import extract_text_from_pdf
from modules.resume_parser import segment_resume_sections, extract_candidate_skills
from modules.job_parser import extract_required_skills
from modules.matcher import compute_match_analysis
from modules.llm_service import LLMService
from modules.report_generator import generate_export_report

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer & Career Assistant",
    page_icon="📄",
    layout="wide"
)

# Initialize LLM Service
llm_service = LLMService()

# Header & Academic Affiliation
st.title("📄 AI-Powered Resume Analyzer & Career Assistant")
st.caption("MCA Academic Project | Abu Zar Reehan (USN: SCA25MCA070) | Dayananda Sagar University (2025–2027)")

# Sidebar for Configuration & Metadata
with st.sidebar:
    st.header("⚙️ Project Controls")
    student_name = st.text_input("Candidate Name", value="Abu Zar Reehan")
    usn = st.text_input("USN", value="SCA25MCA070")
    
    st.markdown("---")
    st.subheader("LLM Status")
    if llm_service.api_available:
        st.success("✅ Google Gemini API Connected")
    else:
        st.info("ℹ️ Running in Local Rule-Based Mode (Add GEMINI_API_KEY in .env for live LLM generation)")
    
    st.markdown("---")
    st.markdown("**Ethical Notice:** Outputs are advisory and intended for skill gap analysis and interview preparation, not automated hiring decisions.")

# Main Input Layout (Two Columns)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("1. Upload Resume (PDF)")
    uploaded_file = st.file_uploader("Select candidate resume", type=["pdf"])
    
    resume_text = ""
    candidate_skills = []
    if uploaded_file is not None:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > MAX_UPLOAD_SIZE_MB:
            st.error(f"File size exceeds maximum limit of {MAX_UPLOAD_SIZE_MB}MB.")
        else:
            resume_text, success, msg = extract_text_from_pdf(uploaded_file.read())
            if success:
                st.success(msg)
                sections = segment_resume_sections(resume_text)
                candidate_skills = extract_candidate_skills(resume_text)
                with st.expander("Extracted Resume Skills & Sections"):
                    st.write("**Detected Skills:**", ", ".join(candidate_skills) if candidate_skills else "None")
                    st.write("**Identified Sections:**", list(sections.keys()))
            else:
                st.error(msg)

with col_right:
    st.subheader("2. Target Job Description")
    sample_jd = (
        "Seeking a Software Engineer with proficiency in Python, REST APIs, SQL, Docker, "
        "and Git. Experience with React or modern frontends, unit testing, and agile workflows is preferred."
    )
    job_description = st.text_area("Paste job requirements or role description", value=sample_jd, height=180)
    job_skills = extract_required_skills(job_description) if job_description else []
    
    if job_skills:
        st.info(f"Target skills identified in job description: {', '.join(job_skills)}")

st.markdown("---")

# Analysis Action
if st.button("🚀 Analyze Alignment & Generate Guidance", type="primary", use_container_width=True):
    if not resume_text:
        st.warning("Please upload a readable PDF resume before running analysis.")
    elif not job_description.strip():
        st.warning("Please provide a job description.")
    else:
        with st.spinner("Analyzing skill alignment and synthesizing career recommendations..."):
            match_data = compute_match_analysis(candidate_skills, job_skills)
            feedback = llm_service.generate_feedback(
                resume_text, job_description, match_data["matched_skills"], match_data["missing_skills"]
            )
            interview_qs = llm_service.generate_interview_questions(
                job_description, match_data["matched_skills"], match_data["missing_skills"]
            )
            
            # Save results in session state
            st.session_state["match_data"] = match_data
            st.session_state["feedback"] = feedback
            st.session_state["interview_qs"] = interview_qs

# Display Results Dashboard
if "match_data" in st.session_state:
    match_data = st.session_state["match_data"]
    feedback = st.session_state["feedback"]
    interview_qs = st.session_state["interview_qs"]
    
    score = match_data["score_percentage"]
    st.subheader(f"📊 Overall Alignment Score: {score}%")
    st.progress(score / 100.0)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Skill Gap Analysis",
        "💡 AI Career Recommendations",
        "🎤 Practice Interview Questions",
        "📥 Export Report"
    ])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.success(f"**Matched Competencies ({match_data['matched_count']})**")
            if match_data["matched_skills"]:
                for s in match_data["matched_skills"]:
                    st.markdown(f"- ✅ **{s}**")
            else:
                st.write("No direct keyword matches found.")
        with c2:
            st.warning(f"**Missing / Un-evidenced Skills ({len(match_data['missing_skills'])})**")
            if match_data["missing_skills"]:
                for s in match_data["missing_skills"]:
                    st.markdown(f"- ⚠️ **{s}** *(Opportunity to acquire or evidence)*")
            else:
                st.write("All required competencies are evidenced in the resume!")
                
    with tab2:
        st.markdown(feedback)
        
    with tab3:
        st.markdown(interview_qs)
        
    with tab4:
        report_md = generate_export_report(student_name, usn, match_data, feedback, interview_qs)
        st.download_button(
            label="📄 Download Complete Evaluation Report (Markdown)",
            data=report_md,
            file_name=f"resume_analysis_{usn}.md",
            mime="text/markdown"
        )
