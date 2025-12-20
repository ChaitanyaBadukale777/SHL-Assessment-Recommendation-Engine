import pandas as pd
import os
import re

def normalize_column(col: str) -> str:
    return (
        col.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

def normalize_url(url: str) -> str:
    if not isinstance(url, str):
        return ""
    url = url.strip().replace("\n", "").replace(" ", "")
    url = url.lower()
    url = url.split("?")[0]
    url = url.rstrip("/")
    url = url.replace("https://www.shl.com/solutions", "https://www.shl.com")
    if url.startswith("/"):
        url = "https://www.shl.com" + url
    return url


def load_catalogue(path: str = "data/SHL_Cleaned_Wide_Format.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Catalog CSV not found at {path}")

    # 🔥 Force-safe CSV read
    df = pd.read_csv(
        path,
        encoding="latin1",
        engine="python"
    )

    # Normalize column names
    df.columns = [normalize_column(c) for c in df.columns]

    df.fillna("", inplace=True)

    # 🔴 DEBUG: print columns once
    print("Catalog columns:", df.columns.tolist())

    # ---- FIX COLUMN NAME MISMATCH ----
    # Your CSV likely has "assessment_url" named differently
    url_candidates = [
        "assessment_url",
        "assessment_link",
        "url",
        "link"
    ]

    found_url_col = None
    for c in url_candidates:
        if c in df.columns:
            found_url_col = c
            break

    if not found_url_col:
        raise ValueError("No assessment URL column found in catalog CSV")

    if found_url_col != "assessment_url":
        df.rename(columns={found_url_col: "assessment_url"}, inplace=True)

    # Normalize URLs
    df["assessment_url"] = df["assessment_url"].apply(normalize_url)

    # Create assessment_name if missing
    if "assessment_name" not in df.columns:
        df["assessment_name"] = (
            df["assessment_url"]
            .str.split("/")
            .str[-1]
            .str.replace("-", " ", regex=False)
            .str.title()
        )

    # Build searchable text
    if "text" not in df.columns:
        text_cols = [c for c in df.columns if c not in ["assessment_url"]]
        df["text"] = df[text_cols].astype(str).agg(" ".join, axis=1)

    df["text"] = df["text"].str.lower()

    return df
