from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    """Embed text by chunking into sentences and averaging embeddings"""
    # Split into meaningful chunks (sentences or bullet points)
    chunks = []
    for line in text.split('\n'):
        line = line.strip()
        if len(line) > 20:  # Only meaningful chunks
            chunks.append(line)
    
    if not chunks:
        # Fallback to sentence splitting if no good chunks
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        sentences = nltk.sent_tokenize(text)
        chunks = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if not chunks:
        # Last resort: split by periods
        chunks = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
    
    if not chunks:
        # If still no chunks, use the whole text
        chunks = [text]
    
    # Embed each chunk and average
    embeddings = model.encode(chunks)
    return np.mean(embeddings, axis=0)

def compute_similarity(resume_text: str, job_text: str) -> float:
    """Compute similarity using chunked embeddings for better accuracy"""
    resume_vec = embed_text(resume_text)
    job_vec = embed_text(job_text)
    sim_score = cosine_similarity([resume_vec], [job_vec])[0][0]
    return round(float(sim_score), 4)

# resume_parser.py
import fitz  # PyMuPDF
from fastapi import UploadFile

def extract_text_from_pdf(file: UploadFile) -> str:
    text = ""
    with fitz.open(stream=file.file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text: str) -> list[str]:
    doc = nlp(text)
    keywords = set()
    
    # Common irrelevant words to filter out
    irrelevant_words = {
        'job', 'work', 'position', 'role', 'company', 'team', 'project', 'time',
        'year', 'month', 'day', 'week', 'hour', 'minute', 'second', 'duration',
        'demo', 'example', 'sample', 'test', 'trial', 'arr', 'rag', 'tune',
        'energy', 'turn', 'production', '📍', '🎯', '🚀', '💡', '📊', '📈'
    }
    
    for token in doc:
        # Only consider nouns, proper nouns, and verbs
        if token.pos_ in ["NOUN", "PROPN", "VERB"] and not token.is_stop:
            # Filter out irrelevant words and short terms
            lemma = token.lemma_.lower()
            if (len(lemma) >= 3 and 
                lemma not in irrelevant_words and
                not re.match(r'^[^\w\s]+$', lemma) and  # No pure symbols
                not re.match(r'^\d+$', lemma)):  # No pure numbers
                keywords.add(lemma)
    
    return list(keywords)

def find_missing_keywords(resume_text: str, job_text: str) -> list[str]:
    job_keywords = extract_keywords(job_text)
    resume_text = resume_text.lower()
    
    # Filter out keywords that are already present in resume
    missing = [kw for kw in job_keywords if kw not in resume_text]
    
    # Sort by relevance (longer, more specific terms first)
    missing.sort(key=lambda x: (len(x), x), reverse=True)
    
    return missing[:15]  # Limit to 15 most relevant missing keywords

def generate_suggestions(missing_keywords: list[str]) -> list[str]:
    if not missing_keywords:
        return ["Your resume appears to cover most of the job requirements well!"]
    
    suggestions = []
    
    # Group similar keywords
    tech_keywords = [kw for kw in missing_keywords if any(tech in kw for tech in ['python', 'java', 'javascript', 'react', 'angular', 'node', 'sql', 'aws', 'docker', 'kubernetes', 'api', 'git', 'html', 'css'])]
    soft_skill_keywords = [kw for kw in missing_keywords if any(skill in kw for skill in ['leadership', 'communication', 'collaboration', 'problem', 'analysis', 'planning', 'organization'])]
    other_keywords = [kw for kw in missing_keywords if kw not in tech_keywords and kw not in soft_skill_keywords]
    
    if tech_keywords:
        suggestions.append(f"Highlight your technical skills: {', '.join(tech_keywords[:5])}")
    
    if soft_skill_keywords:
        suggestions.append(f"Emphasize soft skills: {', '.join(soft_skill_keywords[:5])}")
    
    if other_keywords:
        suggestions.append(f"Consider adding experience with: {', '.join(other_keywords[:5])}")
    
    return suggestions[:5]  # Limit to 5 meaningful suggestions
