"""
Matching Engine and Gap Analysis.
Calculates alignment score and classifies matched vs unevidenced requirements.
"""
def compute_match_analysis(candidate_skills: list[str], job_skills: list[str]) -> dict:
    """Computes Jaccard/overlap alignment and isolates skill gaps."""
    c_set = set(s.lower() for s in candidate_skills)
    j_set = set(s.lower() for s in job_skills)
    
    if not j_set:
        return {
            "score_percentage": 0,
            "matched_skills": list(candidate_skills),
            "missing_skills": [],
            "total_job_skills": 0,
            "matched_count": 0
        }
        
    matched = c_set.intersection(j_set)
    missing = j_set - c_set
    
    score = (len(matched) / len(j_set)) * 100
    
    return {
        "score_percentage": round(score, 1),
        "matched_skills": sorted([s.title() for s in matched]),
        "missing_skills": sorted([s.title() for s in missing]),
        "total_job_skills": len(j_set),
        "matched_count": len(matched)
    }
