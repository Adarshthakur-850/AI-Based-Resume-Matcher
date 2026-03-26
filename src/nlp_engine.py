import spacy
import re
import json

class NLPEngine:
    def __init__(self, skills_path):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback or instructions to download
            print("Model 'en_core_web_sm' not found. Please download it using: python -m spacy download en_core_web_sm")
            self.nlp = spacy.blank("en")
            
        self.skills_db = self._load_skills(skills_path)

    def _load_skills(self, path):
        if not path: return set()
        with open(path, 'r') as f:
            data = json.load(f)
        # Flatten dictionary to set of skills
        skills = set()
        for category in data.values():
            for skill in category:
                skills.add(skill.lower())
        return skills

    def clean_text(self, text):
        doc = self.nlp(text)
        clean_tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
        return " ".join(clean_tokens)

    def extract_skills(self, text):
        text_lower = text.lower()
        found_skills = []
        for skill in self.skills_db:
            # Simple keyword matching for speed/simplicity
            # For more complex matching, matchers or vector similarity could be used
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.append(skill)
        return list(set(found_skills))

    def extract_experience(self, text):
        # Very detailed regex for experience is complex; using simple heuristic for now
        # Creating a placeholder for "Total Experience" reasoning
        # In a real app, this would detect date ranges (e.g. "Jan 2018 - Present")
        
        # Simple heuristic: finding "years" or "years of experience"
        match = re.search(r'(\d+)\+?\s*years?', text.lower())
        if match:
            return int(match.group(1))
        return 0
