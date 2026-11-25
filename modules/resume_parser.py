"""
Resume Section Segmentation and Skill Parsing Module.
"""
import re
from config import COMMON_SKILLS

SECTION_HEADERS = {
    "education": ["education", "academic qualification", "academics", "qualifications"],
    "skills": ["skills", "technical skills", "core competencies", "technologies", "proficiencies"],
    "experience": ["experience", "work experience", "employment history", "internships", "professional experience"],
    "projects": ["projects", "academic projects", "key projects", "personal projects"],
    "certifications": ["certifications", "certificates", "courses", "licenses"]
}

def segment_resume_sections(text: str) -> dict[str, str]:
    """Segment resume text into standard sections based on detected headings."""
    lines = text.split("\n")
    sections = {k: [] for k in SECTION_HEADERS}
    sections["general"] = []
    
    current_section = "general"
    
    for line in lines:
        cleaned = line.strip().lower()
        if not cleaned:
            continue
            
        matched_section = None
        for sec, triggers in SECTION_HEADERS.items():
            if any(re.match(rf"^\s*{re.escape(trig)}\s*:?$", cleaned) for trig in triggers):
                matched_section = sec
                break
                
        if matched_section:
            current_section = matched_section
        else:
            sections[current_section].append(line.strip())
            
    return {k: "\n".join(v).strip() for k, v in sections.items()}

def extract_candidate_skills(text: str) -> list[str]:
    """Identifies skills present in the resume based on the curated taxonomy."""
    text_lower = text.lower()
    found_skills = set()
    for skill in COMMON_SKILLS:
        pattern = rf"(?:\b|\W){re.escape(skill)}(?:\b|\W)"
        if re.search(pattern, text_lower):
            found_skills.add(skill.title())
    return sorted(list(found_skills))
