from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re

# -------------------------------
# Helper functions
# -------------------------------

def extract_duration(text: str) -> int:
    """
    Extract duration in minutes from assessment text.
    """
    if not isinstance(text, str):
        return 0

    text = text.lower()

    patterns = [
        r'completion time.*?=\s*(\d+)',
        r'(\d+)\s*minutes'
    ]

    for p in patterns:
        match = re.search(p, text)
        if match:
            return int(match.group(1))

    return 0


def infer_test_type(text: str):
    """
    Infer test type heuristically from description text.
    """
    if not isinstance(text, str):
        return ["Knowledge & Skills"]

    text = text.lower()
    types = []

    if any(k in text for k in ["programming", "coding", "technical", "knowledge"]):
        types.append("Knowledge & Skills")

    if any(k in text for k in ["behavior", "behaviour", "personality"]):
        types.append("Personality & Behaviour")

    if any(k in text for k in ["aptitude", "ability", "numerical", "logical"]):
        types.append("Ability & Aptitude")

    if any(k in text for k in ["situational", "judgement", "biodata"]):
        types.append("Biodata & Situational Judgement")

    if any(k in text for k in ["simulation", "scenario"]):
        types.append("Simulations")

    return list(set(types)) if types else ["Knowledge & Skills"]


# -------------------------------
# Model & Index
# -------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")
index = None


def build_index(df):
    """
    Build FAISS index from assessment text.
    """
    global index

    embeddings = model.encode(
        df["text"].tolist(),
        show_progress_bar=False,
        convert_to_numpy=True
    ).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)


# -------------------------------
# RAG Recommendation
# -------------------------------

def recommend_rag(df, query: str, top_n: int = 10):
    """
    RAG-based semantic recommendation.
    """
    global index

    if index is None:
        build_index(df)

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    _, indices = index.search(query_embedding, top_n)
    results = df.iloc[indices[0]]

    recommendations = []

    for _, row in results.iterrows():
        recommendations.append({
            "url": row["assessment_url"],
            "name": row["assessment_name"],
            "adaptive_support": row.get("adaptive_support", "No"),
            "description": row.get("description", ""),
            "duration": row.get(
                "duration_minutes",
                extract_duration(row.get("text", ""))
            ),
            "remote_support": row.get("remote_support", "Yes"),
            "test_type": [infer_test_type(row.get("text", ""))[0]]
        })

    return recommendations
