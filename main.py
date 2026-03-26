import os
import argparse
from src.parser import parse_resume
from src.nlp_engine import NLPEngine
from src.matcher import Matcher
from src.ranking import Ranker
from src.report import Reporter

def main():
    parser = argparse.ArgumentParser(description="AI-Based Resume Matcher")
    parser.add_argument("--resumes", type=str, default="data/resumes", help="Path to resumes folder")
    parser.add_argument("--jd", type=str, default="data/job_description.txt", help="Path to job description file")
    args = parser.parse_args()

    # Initialize Modules
    nlp = NLPEngine("data/skills.json")
    matcher = Matcher()
    ranker = Ranker()
    reporter = Reporter("output")

    # 1. Parse Job Description
    if not os.path.exists(args.jd):
        print(f"Error: Job description file {args.jd} not found.")
        return

    with open(args.jd, 'r', encoding='utf-8') as f:
        jd_text = f.read()

    jd_clean = nlp.clean_text(jd_text)
    jd_skills = nlp.extract_skills(jd_text)
    jd_exp = nlp.extract_experience(jd_text) or 2 # Default to 2 if not found
    
    jd_data = {
        "text": jd_clean,
        "skills": jd_skills,
        "required_experience": jd_exp
    }
    
    print(f"Job Description Processed. Found {len(jd_skills)} skills.")

    # 2. Process Resumes
    candidates = []
    
    if not os.path.exists(args.resumes):
        print(f"Error: Resumes directory {args.resumes} not found.")
        return

    for filename in os.listdir(args.resumes):
        file_path = os.path.join(args.resumes, filename)
        if not os.path.isfile(file_path): continue
        
        print(f"Processing {filename}...")
        try:
            raw_text = parse_resume(file_path)
            if not raw_text.strip():
                print(f"Warning: Could not extract text from {filename}")
                continue
                
            clean_text = nlp.clean_text(raw_text)
            skills = nlp.extract_skills(raw_text)
            exp = nlp.extract_experience(raw_text)
            
            # Compute Similarity
            similarity = matcher.compute_similarity(jd_clean, clean_text)
            
            resume_data = {
                "text": clean_text,
                "skills": skills,
                "experience": exp,
                "similarity": similarity
            }
            
            # Score
            scores = ranker.score_candidate(resume_data, jd_data)
            
            candidates.append({
                "filename": filename,
                "score": scores["total_score"],
                "semantic_match": scores["semantic_score"],
                "skill_match": scores["skill_score"],
                "experience_match": scores["experience_score"],
                "skills_found": ", ".join(scores["matched_skills"]),
                "experience_years": exp
            })
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # 3. Report
    if candidates:
        df = reporter.generate_csv(candidates)
        reporter.plot_scores(df)
        print("\n--- Top Candidates ---")
        print(df[["filename", "score", "skills_found"]].head().to_string(index=False))
    else:
        print("No candidates found or processed.")

if __name__ == "__main__":
    main()
