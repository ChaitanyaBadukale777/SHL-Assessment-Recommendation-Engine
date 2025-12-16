from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_similarity(df, job_description, top_n=5):
    corpus = df["skills_assessed"].tolist()
    corpus.append(job_description)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus)

    similarity_scores = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
    df["similarity"] = similarity_scores

    return df.sort_values("similarity", ascending=False).head(top_n)[
        ["assessment_name", "job_family", "job_level", "skills_assessed", "duration_minutes"]
    ].to_dict(orient="records")
