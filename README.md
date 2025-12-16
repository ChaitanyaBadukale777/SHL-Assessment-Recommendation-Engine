# SHL-Assessment-Recommendation-Engine

# SHL Assessment Recommendation Engine

## Problem Statement
Recruiters often struggle to choose the right assessments for a given job role.
This project recommends suitable SHL-style assessments using a mock product catalogue.

## Dataset
A mock SHL product catalogue inspired by the public SHL website.
Attributes include job family, job level, skills, duration, and test type.

## Approaches Used
1. Rule-Based Recommendation
2. NLP Similarity-Based Recommendation (TF-IDF + Cosine Similarity)

## Tech Stack
- Python
- Pandas
- Scikit-learn
- FastAPI

## How to Run
```bash
pip install -r requirements.txt
uvicorn api.app:app --reload
