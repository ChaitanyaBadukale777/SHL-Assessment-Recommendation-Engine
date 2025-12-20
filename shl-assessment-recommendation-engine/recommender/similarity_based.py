from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load embedding model once (important for performance)
_model = SentenceTransformer("all-MiniLM-L6-v2")

# Global FAISS index (built once)
_index = None


def build_index(df):
    """
    Build FAISS index from assessment text.
    Called once when the app starts.
    """
    global _index

    texts = df["text"].tolist()

    embeddings = _model.encode(
        texts,
        show_progress_bar=False,
        convert_to_numpy=True
    ).astype("float32")

    dim = embeddings.shape[1]
    _index = faiss.IndexFlatL2(dim)
    _index.add(embeddings)


def recommend_similarity(df, query: str, top_n: int = 10):
    """
    Semantic similarity-based recommendation using embeddings.
    """
    global _index

    if _index is None:
        build_index(df)

    query_embedding = _model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    _, indices = _index.search(query_embedding, top_n)
    results = df.iloc[indices[0]]

    return results[
        ["assessment_name", "assessment_url"]
    ].to_dict(orient="records")
