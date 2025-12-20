"""
Evaluation Script: Recall@10
---------------------------------
This script evaluates the SHL Assessment Recommendation Engine
using Recall@10 on the provided labeled train dataset.

Flow:
1. Load SHL catalog (377+ assessments)
2. Build semantic index (FAISS + MiniLM)
3. Load labeled train queries
4. Run retrieval
5. Compute Recall@10
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from recommender.data_loader import load_catalogue
from recommender.rag_recommender import recommend_rag


# ==============================
# CONFIG
# ==============================

CATALOG_PATH = "data/SHL_Cleaned_Wide_Format.csv"
TRAIN_PATH = "data/Gen_AI_Dataset.csv"
TOP_K = 10


# ==============================
# HELPERS
# ==============================

def normalize_url(url: str) -> str:
    if not isinstance(url, str):
        return ""
    return (
        url.strip()
        .lower()
        .split("?")[0]
        .rstrip("/")
        .replace("https://www.shl.com/solutions", "https://www.shl.com")
    )


def split_urls(x):
    if isinstance(x, str):
        return [normalize_url(u) for u in x.split("|")]
    return []


def recall_at_10(predicted_urls, true_urls):
    if not true_urls:
        return 0.0
    return len(set(predicted_urls[:10]) & set(true_urls)) / len(true_urls)


# ==============================
# MAIN EVALUATION
# ==============================

def main():
    print("Loading SHL catalog...")
    df_catalog = load_catalogue("../data/SHL_Cleaned_Wide_Format.csv")

    print("Catalog size:", len(df_catalog))

    print("Loading labeled train dataset...")
    train_df = pd.read_csv("../data/Gen_AI_Dataset.csv", encoding="latin1")

    # Fix column names
    train_df.columns = train_df.columns.str.strip().str.lower()

    # Handle BOM issue
    if "ï»¿query" in train_df.columns:
        train_df.rename(columns={"ï»¿query": "query"}, inplace=True)

    # Prepare ground truth URLs
    train_df["true_urls"] = train_df["assessment_url"].apply(split_urls)

    scores = []

    print("\nEvaluating Recall@10...\n")

    for i, row in train_df.iterrows():
        query = row["query"]
        true_urls = row["true_urls"]

        results = recommend_rag(df_catalog, query, top_n=TOP_K)

        predicted_urls = [
            normalize_url(r["url"]) for r in results
        ]

        score = recall_at_10(predicted_urls, true_urls)
        scores.append(score)

        print(f"Query {i+1}: Recall@10 = {score:.2f}")

    mean_recall = sum(scores) / len(scores)

    print("\n==============================")
    print(f"MEAN RECALL@10: {mean_recall:.4f}")
    print("==============================\n")


if __name__ == "__main__":
    main()


