from fastapi import FastAPI,UploadFile,File,Form
from app.modules.users.routes import router as user_router
from contextlib import asynccontextmanager
from app.core.database import engine, Base
import asyncio
from fastapi.staticfiles import StaticFiles
from app.api.resume_router import router as resume_router

@asynccontextmanager
async def life_span(app: FastAPI):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, Base.metadata.create_all, engine)
    yield

    
app = FastAPI(lifespan=life_span)
app.mount("/media", StaticFiles(directory="media"), name="media")
app.include_router(user_router)
app.include_router(resume_router)




# from app.utils import compute_similarity, find_missing_keywords, generate_suggestions,extract_text_from_pdf

# @app.post("/score")
# async def score_resume(
#     resume_file: UploadFile = File(...),
#     job_description: str = Form(...)
# ):
#     resume_data = extract_text_from_pdf(resume_file)
#     print(resume_data)
#     score = compute_similarity(resume_data, job_description)
    
#     missing = find_missing_keywords(resume_data, job_description)
#     suggestions = generate_suggestions(missing)

#     return {
#         "score": score,
#         "suggestions": suggestions
#     }
