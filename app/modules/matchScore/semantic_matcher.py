from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticMatcher:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def calculate_match(self, cv_text: str, job_text: str) -> float:
        cv_chunks = self._chunk_text(cv_text)
        job_chunks = self._chunk_text(job_text)
        
        cv_embeddings = self.model.encode(cv_chunks)
        job_embeddings = self.model.encode(job_chunks)
        
        similarities = np.dot(cv_embeddings, job_embeddings.T)
        max_similarities = np.max(similarities, axis=1)
        
        return np.mean(max_similarities) * 100
    
    @staticmethod
    def _chunk_text(text: str, max_length: int = 500) -> list:
        words = text.split()
        return [' '.join(words[i:i+max_length]) 
                for i in range(0, len(words), max_length)]