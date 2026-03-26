behavior_profile = {
    "most_active_hour": 8,
    "favorite_day": "Sunday",
    "avg_hours_between_trades": 245.25,
    "max_value_zscore": 3.51,
    "max_trades_per_day": 2,
    "error_rate": 0.0,
    "most_common_defi_action": "transfer(address recipient, uint256 amount)"
}

def score_emotional_risk(behavior_profile):
    risk_score = 0
    reasons = []

    if behavior_profile["avg_hours_between_trades"] < 24:
        risk_score += 20
        reasons.append("Trades too frequently — signs of impulsive behavior.")

    if behavior_profile["max_trades_per_day"] > 3:
        risk_score += 20
        reasons.append("Multiple trades in a single day detected.")

    if behavior_profile["max_value_zscore"] > 2:
        risk_score += 25
        reasons.append("Unusually large transaction detected compared to normal behavior.")

    if behavior_profile["error_rate"] > 10:
        risk_score += 20
        reasons.append("High transaction failure rate — signs of rushed trading.")

    if behavior_profile["most_active_hour"] >= 0 and behavior_profile["most_active_hour"] <= 5:
        risk_score += 15
        reasons.append("Trades mostly at night — emotional decisions more likely.")

    return {
        "risk_score": min(risk_score, 100),
        "reasons": reasons
    }

def get_verdict(risk_score):
    if risk_score >= 60:
        return "🔴 EMOTIONAL PATTERN DETECTED"
    elif risk_score >= 30:
        return "🟡 CAUTION"
    return "🟢 CLEAN SIGNAL"

def evaluate_wallet(behavior_profile):
    result = score_emotional_risk(behavior_profile)
    verdict = get_verdict(result["risk_score"])
    return {
        "verdict": verdict,
        "risk_score": result["risk_score"],
        "reasons": result["reasons"]
    }

evaluation = evaluate_wallet(behavior_profile)
print(evaluation)