from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Set

class GapAnalyzer:
    def __init__(self, max_keywords: int = 20):
        self.max_keywords = max_keywords
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=50)
    
    def analyze(self, cv_text: str, job_text: str, job_skills: Set[str]) -> Dict:
        gaps = {
            'missing_explicit_keywords': [],
            'missing_skills': [],
            'weak_areas': [],
            'suggestions': []
        }
        
        #xxtract important keywords
        important_keywords = self._extract_keywords(job_text)
        
        #find missing keywords
        cv_lower = cv_text.lower()
        gaps['missing_explicit_keywords'] = [
            kw for kw in important_keywords if kw not in cv_lower
        ]
        
        #find missing skills
        gaps['missing_skills'] = [
            skill for skill in job_skills if skill.lower() not in cv_lower
        ]
        
        #generate suggestions
        gaps['suggestions'] = self._generate_suggestions(gaps)
        
        return gaps
    
    def _extract_keywords(self, text: str) -> List[str]:
        tfidf_matrix = self.vectorizer.fit_transform([text])
        feature_names = self.vectorizer.get_feature_names_out()
        # Get top keywords by TF-IDF score
        top_indices = tfidf_matrix[0].argsort()[-self.max_keywords:][::-1]
        return [feature_names[i] for i in top_indices]
    
    def _generate_suggestions(self, gaps: Dict) -> List[str]:
        suggestions = []
        
        if gaps['missing_skills']:
            suggestions.append(
                f"Add these skills: {', '.join(gaps['missing_skills'][:5])}"
            )
        
        if len(gaps['missing_explicit_keywords']) > 10:
            suggestions.append(
                "Your CV lacks common keywords for this role. "
                "Review the job description carefully."
            )
        
        return suggestions