"""
Job Description Parser and Requirement Normalizer.
"""
import re
from config import COMMON_SKILLS

def extract_required_skills(job_description: str) -> list[str]:
    """Identifies required technical skills from the target job description."""
    jd_lower = job_description.lower()
    required = set()
    for skill in COMMON_SKILLS:
        pattern = rf"(?:\b|\W){re.escape(skill)}(?:\b|\W)"
        if re.search(pattern, jd_lower):
            required.add(skill.title())
    return sorted(list(required))
