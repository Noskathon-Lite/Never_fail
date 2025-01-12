from fastapi import FastAPI
from backend.services.plagiarism_service import check_plagiarism
from backend.models import DocumentRequest

app = FastAPI()

@app.post("/check_plagiarism")
def check_plagiarism_route(request: DocumentRequest):
    return check_plagiarism(request.text)
