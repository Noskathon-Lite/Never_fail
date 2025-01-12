from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from backend.utils import load_documents

app = FastAPI()

# BaseModel for request
class PlagiarismRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Welcome to the Plagiarism Checker API"}

@app.post("/check-plagiarism")
def check_plagiarism(request: PlagiarismRequest):
    query_text = request.query
    
    # Load all documents
    documents = load_documents("data/documents/")
    if not documents:
        raise HTTPException(status_code=400, detail="No documents found for comparison.")
    
    # Add the query text to the list of documents
    documents.append(query_text)

    # Compute TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Calculate cosine similarity
    query_vector = tfidf_matrix[-1]
    similarities = cosine_similarity(query_vector, tfidf_matrix[:-1])
    
    # Format the response
    response = [
        {"document": f"doc{i + 1}.txt", "similarity": round(score * 100, 2)}
        for i, score in enumerate(similarities[0])
    ]
    
    # Sort by similarity
    response = sorted(response, key=lambda x: x["similarity"], reverse=True)
    
    return {"query": query_text, "results": response}
