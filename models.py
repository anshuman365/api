import numpy as np

def score_candidate(resume_data, job_match_score):
    """
    Assigns an AI-based score to a candidate based on extracted data and job match percentage.
    """
    score = 0
    
    # Give weightage to job match percentage
    score += job_match_score * 0.6  

    # Give weightage to experience
    experience = resume_data.get("experience", "Unknown")
    if experience.isdigit():
        score += int(experience) * 5  

    # Give weightage to skill match
    skills = len(resume_data.get("skills", []))
    score += skills * 10  
    
    # Normalize the score to a range of 0-100
    return min(score, 100)