from fastapi import FastAPI
from pydantic import BaseModel
from recommender.data_loader import load_catalogue
from recommender.rule_based import recommend_rule_based
from recommender.similarity_based import recommend_similarity

app = FastAPI(title="SHL Assessment Recommendation Engine")

df = load_catalogue()

class RuleBasedRequest(BaseModel):
    job_family: str
    job_level: str
    skills: list[str]

class SimilarityRequest(BaseModel):
    job_description: str

@app.post("/recommend/rule-based")
def rule_based_recommendation(request: RuleBasedRequest):
    return {
        "recommended_assessments": recommend_rule_based(
            df,
            request.job_family,
            request.job_level,
            request.skills
        )
    }

@app.post("/recommend/similarity")
def similarity_recommendation(request: SimilarityRequest):
    return {
        "recommended_assessments": recommend_similarity(
            df,
            request.job_description
        )
    }
