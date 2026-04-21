# modules/ai_insights.py

def generate_insights(scores, avg, student_name):
    """
    Improved rule-based AI insights engine for education analytics
    """

    if not scores:
        return "No academic data available yet for analysis."

    insights = []

    # =========================
    # 1. PERFORMANCE LEVEL
    # =========================
    if avg >= 75:
        insights.append(f"🟢 {student_name} is performing at an excellent academic level.")
    elif avg >= 50:
        insights.append(f"🟡 {student_name} is performing at an average level with room for improvement.")
    else:
        insights.append(f"🔴 {student_name} is performing below expected level and needs academic support.")

    # =========================
    # 2. TREND ANALYSIS
    # =========================
    if len(scores) >= 3:
        last_scores = [s[2] for s in scores[-3:]]

        if last_scores[2] > last_scores[1] > last_scores[0]:
            insights.append("📈 Strong upward trend detected in recent performance.")
        elif last_scores[2] < last_scores[1] < last_scores[0]:
            insights.append("📉 Continuous decline detected in recent performance.")
        else:
            insights.append("📊 Performance is fluctuating without a clear trend.")

    elif len(scores) >= 2:
        recent = scores[-1][2]
        previous = scores[-2][2]

        if recent > previous:
            insights.append("📈 Recent improvement detected.")
        elif recent < previous:
            insights.append("📉 Recent decline detected.")
        else:
            insights.append("📊 No significant change in performance.")

    # =========================
    # 3. RISK ANALYSIS
    # =========================
    if avg < 40:
        insights.append("🚨 Critical risk: Immediate intervention required.")
    elif avg < 50:
        insights.append("⚠️ High risk: Student is at risk of academic failure.")
    elif avg < 70:
        insights.append("🟡 Moderate risk: Monitoring recommended.")
    else:
        insights.append("🟢 Low risk: Student is in a safe academic zone.")

    # =========================
    # 4. SIMPLE RECOMMENDATION ENGINE
    # =========================
    if avg < 50:
        insights.append("💡 Recommendation: Increase revision time and provide tutoring support.")
    elif avg < 70:
        insights.append("💡 Recommendation: Focus on weak subjects and practice consistently.")
    else:
        insights.append("💡 Recommendation: Encourage advanced exercises to maintain excellence.")

    return "\n".join(insights)