# services/skill_extractor.py
import re
from typing import Set, List
from pathlib import Path

class SkillExtractor:
    def __init__(self, skill_file_path: str = None):
        # Load comprehensive skill database  (future enhancememnt)
        self.skills = self._load_skill_database()
        
    def _load_skill_database(self) -> Set[str]:
        """Load skills from multiple sources"""
        skills = set()
        
        # Common tech skills
        tech_skills = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
            'swift', 'kotlin', 'php', 'html', 'css', 'sql', 'nosql', 'bash', 'powershell',
            
            # Frameworks & Libraries
            'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'fastapi',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'jquery',
            'bootstrap', 'tailwind', 'sass', 'node.js', '.net', 'laravel', 'rails',
            
            # Databases
            'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
            'oracle', 'sqlite', 'dynamodb', 'firebase',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions',
            'terraform', 'ansible', 'prometheus', 'grafana', 'elk', 'splunk',
            
            # Data Science & ML
            'machine learning', 'deep learning', 'nlp', 'computer vision', 'data analysis',
            'data visualization', 'statistics', 'a/b testing', 'forecasting', 'optimization',
            
            # Project Management & Soft Skills
            'agile', 'scrum', 'kanban', 'jira', 'confluence', 'leadership', 'communication',
            'teamwork', 'problem solving', 'critical thinking', 'time management',
        }
        
        # Business & Domain skills
        business_skills = {
            'project management', 'product management', 'business analysis', 'marketing',
            'sales', 'customer service', 'finance', 'accounting', 'hr', 'recruiting',
            'negotiation', 'presentation', 'reporting', 'forecasting', 'budgeting',
        }
        
        skills.update(tech_skills)
        skills.update(business_skills)
        
        # Load from file if exists (optional)
        # self._load_from_file(skills)
        
        return skills
    
    def extract_skills(self, text: str) -> Set[str]:
        """Extract skills from job description text"""
        found_skills = set()
        text_lower = text.lower()
        
        # Check each skill
        for skill in self.skills:
            # Use word boundaries for exact matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        # Also look for skill patterns like "Experience with X" or "Knowledge of Y"
        skill_patterns = [
            r'experience with ([\w\s]+?)(?:\.|,)',
            r'knowledge of ([\w\s]+?)(?:\.|,)',
            r'proficient in ([\w\s]+?)(?:\.|,)',
            r'skilled in ([\w\s]+?)(?:\.|,)',
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                # Clean and add potential skills
                potential_skill = match.strip()
                if len(potential_skill.split()) <= 3:  # Short phrases only
                    found_skills.add(potential_skill)
        
        return found_skills