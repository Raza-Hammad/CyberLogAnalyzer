def calculate_risk(row):
    score = 0

    if row["login_failed"] == 1:
        score += 30

    if row["is_night"] == 1:
        score += 20

    if row["anomaly_score"] < 0:
        score += 40

    return min(score, 100)
