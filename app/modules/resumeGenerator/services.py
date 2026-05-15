from huggingface_hub import InferenceClient
from typing import Dict, List

class ResumeGeneratorAPI:
    def __init__(self, api_token: str = None):
        self.client = InferenceClient(
            model="kiritps/resume-ai-assistant",
            token=api_token
        )

    def generate_resume(self, cv_text: str, job_text: str, gaps: dict) -> str:
        prompt = f"""
        You are a resume generator. you generate a resume based on the cv and job description. you are accurate and respect the ats standard format.
        here is the job description:
        {job_text}
        here is the cv:
        {cv_text}
        here is the gaps:
        {gaps}
        generate the resume based on the above information.
        """
        response = self.client.text_generation(
            prompt=prompt,
            max_new_tokens=800,
            temperature=0.3,
            do_sample=True,
            return_full_text=False
        )
        return response