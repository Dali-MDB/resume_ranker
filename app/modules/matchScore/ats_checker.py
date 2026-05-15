from typing import List, Dict, Any

class ATSChecker:
    def __init__(self):
        self.checks = [
            self._check_length,
            self._check_headers,
            self._check_formatting,
            self._check_contact_info
        ]
    
    def analyze(self, cv_text: str) -> Dict[str, Any]:
        warnings = []
        score = 100
        
        #convert into lower
        cv_text= cv_text.lower()
        
       
        
        #check length
        score, new_warnings = self._check_length(cv_text, score)
        if new_warnings:
            warnings.append(new_warnings)
        
        
        #check Standard section headers
        score, new_warnings = self._check_headers(cv_text, score)
        if new_warnings:
            for warning in new_warnings:
                warnings.append(warning)
        
        
        #check Complex formatting indicators
        score, new_warning = self._check_formatting(cv_text, score)
        if new_warning:
            warnings.append(new_warning)
        
      
        #check Contact info
        score, new_warning = self._check_contact_info(cv_text, score)
        if new_warning:
            warnings.append(new_warning)
        
        return {
            'ats_score': max(0, score),
            'warnings': warnings,
            'is_ats_friendly': score >= 70
        }
    
    def _check_length(self, text: str, score: int) -> tuple:
        words = len(text.split())
        if words < 300:
            return score - 15, "CV too short (<300 words)"
        elif words > 800:
            return score - 10, "CV may be too long for ATS (>800 words)"
        return score, None
    
    def _check_headers(self, text: str, score: int) -> tuple:
        required = ['experience', 'education', 'skills']
        missing = [sec for sec in required if sec not in text]
        if missing:
            warnings = [f"Missing '{sec}' section" for sec in missing]
            return score - (10 * len(missing)), warnings
        return score, []
    
    def _check_formatting(self, text: str, score: int) -> tuple:
        if 'table' in text or 'column' in text:
            return score - 20, ["Avoid tables/columns - ATS may misread"]
        return score, []
    
    def _check_contact_info(self, text: str, score: int) -> tuple:
        if '@' not in text or ('phone' not in text and 'tel' not in text):
            return score - 15, ["Contact info incomplete or missing"]
        return score, []