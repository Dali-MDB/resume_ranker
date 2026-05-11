from fastapi import FastAPI,UploadFile,File,Form

app = FastAPI()



from app.utils import compute_similarity, find_missing_keywords, generate_suggestions,extract_text_from_pdf

@app.post("/score")
async def score_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_data = extract_text_from_pdf(resume_file)
    print(resume_data)
    score = compute_similarity(resume_data, job_description)
    
    missing = find_missing_keywords(resume_data, job_description)
    suggestions = generate_suggestions(missing)

    return {
        "score": score,
        "suggestions": suggestions
    }
