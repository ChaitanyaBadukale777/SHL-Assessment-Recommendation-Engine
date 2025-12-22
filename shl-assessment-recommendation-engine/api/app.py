from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from recommender.data_loader import load_catalogue
from recommender.rag_recommender import recommend_rag

app = FastAPI(title="SHL Assessment Recommendation Engine")

# 🔥 CORS FIX (THIS IS REQUIRED)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = load_catalogue()

class RecommendRequest(BaseModel):
    query: str
    top_k: int = 10

@app.post("/recommend")
def recommend(request: RecommendRequest):
    return {
        "recommended_assessments": recommend_rag(
            df,
            request.query,
            request.top_k
        )
    }
