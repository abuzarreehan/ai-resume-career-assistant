"""
Standardized prompts for LLM evaluations.
"""
def build_resume_feedback_prompt(resume_text: str, job_description: str, matched_skills: list, missing_skills: list) -> str:
    return f"""You are an expert academic and technical career coach evaluating a candidate's resume against a job description.

RESUME CONTEXT:
\"\"\"
{resume_text[:2500]}
\"\"\"

TARGET JOB DESCRIPTION:
\"\"\"
{job_description[:1500]}
\"\"\"

SKILL GAP ANALYSIS:
- Matched Skills: {', '.join(matched_skills) if matched_skills else 'None identified'}
- Un-evidenced / Missing Skills: {', '.join(missing_skills) if missing_skills else 'None identified'}

Please provide a structured, encouraging evaluation with these exact sections:
1. Executive Alignment Summary: 2-3 sentences on candidate fit.
2. High-Impact Resume Enhancements: 3 specific bullet points on how to better highlight projects and experience.
3. 4-Week Targeted Learning Roadmap: Actionable steps to bridge the missing skill gaps.
"""

def build_interview_prep_prompt(job_description: str, matched_skills: list, missing_skills: list) -> str:
    return f"""Based on the target role below and the candidate's skills profile:
Role & Job Description: {job_description[:1000]}
Verified Skills: {', '.join(matched_skills[:8])}
Areas Needing Growth: {', '.join(missing_skills[:5])}

Generate 5 role-specific interview practice questions:
- 2 Technical Concept Questions (testing core verified competencies)
- 2 Problem-Solving / Project Architecture Scenarios
- 1 Behavioral Question (assessing self-directed learning and skill adaptation)

For each question, add a 1-sentence tip on what interviewers look for.
"""
