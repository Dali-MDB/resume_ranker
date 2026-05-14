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
    