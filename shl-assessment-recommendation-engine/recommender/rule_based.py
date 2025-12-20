# recommender/rule_based.py

def recommend_rule_based(df, query, top_n=5):
    """
    Simple keyword-based baseline recommender.
    This is used as a baseline before semantic (RAG) retrieval.
    """

    query_terms = query.lower().split()
    scores = []

    for _, row in df.iterrows():
        text = row["text"].lower()
        score = sum(1 for term in query_terms if term in text)
        scores.append(score)

    df = df.copy()
    df["score"] = scores

    results = df.sort_values("score", ascending=False).head(top_n)

    return results[
        ["assessment_name", "assessment_url"]
    ].to_dict(orient="records")
