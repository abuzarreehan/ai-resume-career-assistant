"""
Report Generator for exporting analysis summaries in Markdown format.
"""
from datetime import datetime

def generate_export_report(student_name: str, usn: str, match_data: dict, feedback_text: str, questions_text: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""# AI Resume Analyzer & Career Assistant Evaluation Report
**Student Name:** {student_name or 'Candidate'}
**USN:** {usn or 'N/A'}
**Generated On:** {timestamp}

---

## 1. Skill Alignment Overview
- **Alignment Score:** {match_data.get('score_percentage', 0)}%
- **Matched Skills ({match_data.get('matched_count', 0)}):** {', '.join(match_data.get('matched_skills', [])) or 'None'}
- **Missing / Growth Skills ({len(match_data.get('missing_skills', []))}):** {', '.join(match_data.get('missing_skills', [])) or 'None'}

---

## 2. Generative AI Evaluation & Recommendations
{feedback_text}

---

## 3. Role-Specific Interview Questions
{questions_text}

---
*Notice: This report was prepared with the AI Resume Analyzer & Career Assistant for academic and career development guidance.*
"""
