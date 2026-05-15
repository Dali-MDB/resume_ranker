# services/match_score_service.py (Orchestrator)
from .semantic_matcher import SemanticMatcher
from .ats_checker import ATSChecker
from .gap_analyzer import GapAnalyzer
from .skills_extractor import SkillExtractor

class MatchScoreService:
    def __init__(self):
        self.semantic_matcher = SemanticMatcher()
        self.ats_checker = ATSChecker()
        self.gap_analyzer = GapAnalyzer()
        self.skills_extractor = SkillExtractor()
    
    def calculate_semantic_match(self, cv_text: str, job_text: str) -> float:
        return self.semantic_matcher.calculate_match(cv_text, job_text)
    
    def ats_simulation(self, cv_text: str) -> dict:
        return self.ats_checker.analyze(cv_text)
    
    def analyze_gaps(self, cv_text: str, job_text: str) -> dict:
        job_skills = self.skills_extractor.extract_skills(job_text)
        return self.gap_analyzer.analyze(cv_text, job_text, job_skills)
    
    def full_analysis(self, cv_text: str, job_text: str) -> dict:
        """Complete analysis combining all services"""
        return {
            'semantic_match': self.calculate_semantic_match(cv_text, job_text),
            'ats_analysis': self.ats_simulation(cv_text),
            'gap_analysis': self.analyze_gaps(cv_text, job_text)
        }