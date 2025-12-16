def recommend_rule_based(df, job_family, job_level, skills, top_n=5):
    skills = [s.lower() for s in skills]

    scores = []

    for _, row in df.iterrows():
        score = 0

        if job_family.lower() in row["job_family"].lower():
            score += 3

        if job_level.lower() in row["job_level"].lower():
            score += 2

        assessment_skills = row["skills_assessed"].lower().split()
        skill_match = len(set(skills) & set(assessment_skills))
        score += skill_match * 2

        scores.append(score)

    df["score"] = scores
    result = df.sort_values("score", ascending=False)

    return result.head(top_n)[
        ["assessment_name", "job_family", "job_level", "skills_assessed", "duration_minutes"]
    ].to_dict(orient="records")
