from sentence_transformers import SentenceTransformer, util
import numpy as np



class MatchScoreService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def calculate_semantic_match(self, cv_text, job_text):
        # Split into chunks (avoid 512 token limit)
        cv_chunks = self.chunk_text(cv_text, max_length=500)
        job_chunks = self.chunk_text(job_text, max_length=500)
        
        # Encode
        cv_embeddings = self.model.encode(cv_chunks)
        job_embeddings = self.model.encode(job_chunks)
        
        # Get max similarity between chunks
        similarities = np.dot(cv_embeddings, job_embeddings.T)
        max_similarities = np.max(similarities, axis=1)
        
        return np.mean(max_similarities) * 100

    def chunk_text(self, text, max_length=500):
        words = text.split()
        chunks = []
        for i in range(0, len(words), max_length):
            chunks.append(' '.join(words[i:i+max_length]))
        return chunks
    
        
    def check_length(self, cv_text: str, score:int):
        words = len(cv_text.split())
        new_warnings  = None
        if words < 300:
            new_warnings = "CV too short (<300 words)"
            score -= 15
        elif words > 800:
            new_warnings = "CV may be too long for ATS (>800 words)"
            score -= 10

        return score, new_warnings
    
    def check_headers(selfl, cv_text:str, score:int):
        required_sections = ['experience', 'education', 'skills']
        new_warnings = []
        for section in required_sections:
            if section not in cv_text:
                new_warnings.append(f"Missing '{section}' section")
                score -= 10
        return score, new_warnings
    
    def check_complex_formatting(self, cv_text:str, score:int):
        new_warning = []
        if 'table' in cv_text or 'column' in cv_text:
            new_warning.append("Avoid tables/columns - ATS may misread")
            score -= 20
        return score, new_warning

    def check_contact_info(self, cv_text:str, score:int):
        new_warning = []
        if '@' not in cv_text or ('phone' not in cv_text or 'tel' not in cv_text):
            new_warning.append("Contact info incomplete or missing")
            score -= 15
        return score, new_warning

    def ats_simulation(self, cv_text:str):
        warnings = []
        score = 100

        #convert into lower
        cv_text= cv_text.lower()
        
       
        
        #check length
        score, new_warnings = self.check_length(cv_text, score)
        if new_warnings:
            warnings.append(new_warnings)
        
        
        #check Standard section headers
        score, new_warnings = self.check_headers(cv_text, score)
        if new_warnings:
            for warning in new_warnings:
                warnings.append(warning)
        
        
        #check Complex formatting indicators
        score, new_warning = self.check_complex_formatting(cv_text, score)
        if new_warning:
            warnings.append(new_warning)
        
      
        #check Contact info
        score, new_warning = self.check_contact_info(cv_text, score)
        if new_warning:
            warnings.append(new_warning)
        
        return {
            'ats_score': max(0, score),
            'warnings': warnings,
            'is_ats_friendly': score >= 70
        }
        