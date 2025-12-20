from fastapi import FastAPI
from pydantic import BaseModel, Field
from recommender.data_loader import load_catalogue
from recommender.rag_recommender import recommend_rag, build_index

app = FastAPI(title="SHL Assessment Recommendation Engine")

# Load catalogue once
df = load_catalogue()

# Build FAISS index at startup (recommended)
build_index(df)


class RecommendRequest(BaseModel):
    query: str = Field(..., description="Natural language query or job description")
    top_k: int = Field(10, ge=5, le=10, description="Number of recommendations (5–10)")


@app.post("/recommend")
def recommend(request: RecommendRequest):
    return {
        "recommended_assessments": recommend_rag(
            df,
            request.query,
            request.top_k
        )
    }
