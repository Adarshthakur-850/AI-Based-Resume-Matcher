class Ranker:
    def __init__(self, weights={'semantic': 0.5, 'skills': 0.3, 'experience': 0.2}):
        self.weights = weights

    def score_candidate(self, resume_data, jd_data):
        # 1. Semantic Score (0-1)
        semantic_score = resume_data['similarity']
        
        # 2. Skill Score (0-1)
        # Intersection of resume skills and JD skills
        jd_skills = set(jd_data['skills'])
        res_skills = set(resume_data['skills'])
        
        if not jd_skills:
            skill_score = 0
        else:
            intersection = jd_skills.intersection(res_skills)
            skill_score = len(intersection) / len(jd_skills)
            
        # 3. Experience Score (0-1, normalized)
        # Cap experience score at 10 years for normalization
        exp_score = min(resume_data['experience'] / max(1, jd_data['required_experience']), 1.0)
        
        # Weighted Sum
        final_score = (
            self.weights['semantic'] * semantic_score +
            self.weights['skills'] * skill_score +
            self.weights['experience'] * exp_score
        )
        
        return {
            "total_score": round(final_score * 100, 2),
            "semantic_score": round(semantic_score * 100, 2),
            "skill_score": round(skill_score * 100, 2),
            "experience_score": round(exp_score * 100, 2),
            "matched_skills": list(res_skills.intersection(jd_skills))
        }
