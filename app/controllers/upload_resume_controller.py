import os

from fastapi import UploadFile

from app.modules.cvExtraction.services import CvExtractionService
from app.modules.matchScore.services import MatchScoreService
from app.modules.webScraping.services import WebScrapingService

MEDIA_DIR = "media"


async def upload_resume_controller(
    file: UploadFile,
    job_url: str,
    web_scraping_service: WebScrapingService,
    cv_extraction_service: CvExtractionService,
    match_score_service: MatchScoreService,
):
    job_description = web_scraping_service.scrape_job(job_url)

    file_type = file.content_type.split("/")[1]
    if not file_type or file_type not in ["pdf", "docx"]:
        raise Exception("Invalid file type")

    file_path = os.path.join(MEDIA_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    cv_text = cv_extraction_service.extract_cv_text(file_path, file_type)
    analysis = match_score_service.full_analysis(cv_text, job_description)

    return analysis
