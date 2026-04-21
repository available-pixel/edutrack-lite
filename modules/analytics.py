def calculate_risk(avg_score):
    if avg_score < 50:
        return "🚨 At Risk"
    elif avg_score < 70:
        return "⚠️ Needs Attention"
    else:
        return "✅ Stable"