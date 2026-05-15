from fastapi import APIRouter, UploadFile, File, Form, Depends
from app.controllers.upload_resume_controller import upload_resume_controller
from app.modules.webScraping.services import WebScrapingService
from app.modules.cvExtraction.services import CvExtractionService
from app.modules.matchScore.services import MatchScoreService

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/upload_resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_url: str = Form(...),
    web_scraping_service: WebScrapingService = Depends(WebScrapingService),
    cv_extraction_service: CvExtractionService = Depends(CvExtractionService),
    match_score_service: MatchScoreService = Depends(MatchScoreService),
):
    return await upload_resume_controller(
        file,
        job_url,
        web_scraping_service,
        cv_extraction_service,
        match_score_service,
    )
