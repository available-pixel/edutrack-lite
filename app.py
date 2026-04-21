import pandas as pd
import numpy as np
import streamlit as st
from modules.students import create_student, list_students
from modules.performance import record_score, get_student_performance
from modules.analytics import calculate_risk
from modules.ai_insights import generate_insights
from modules.report import generate_student_report, generate_all_students_report
from streamlit_pdf_viewer import pdf_viewer
import datetime

from database.queries import (
    get_all_subjects,
    add_subject,
    delete_student,
    reset_database,
    get_student_count,
    get_subject_count,
    get_all_scores,
    delete_score
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="EduTrack Lite", layout="wide")

# =========================
# SIDEBAR NAVIGATION
# =========================
menu = st.sidebar.radio(
    "📌 Navigation",
    [
        "📊 Dashboard",
        "👨‍🎓 Students",
        "📚 Subjects",
        "📝 Scores",
        "📈 Analytics",
        "📄 Reports",
        "🏆 Leaderboard",
        "⚠️ Admin"
    ]
)

# =========================
# TITLE
# =========================
st.title("📊 EduTrack Lite")
st.subheader("Student Progress Tracker for Low-Resource Schools")

# =========================
# 📊 DASHBOARD
# =========================
if menu == "📊 Dashboard":

    st.header("📊 EduTrack Overview Dashboard")

    students = list_students()
    scores = get_all_scores()

    # =========================
    # KPI CALCULATION
    # =========================
    total_students = get_student_count()
    total_subjects = get_subject_count()

    avg_score = 0
    if scores:
        avg_score = round(sum([s[0] for s in scores]) / len(scores), 2)

    at_risk = 0
    for s in students:
        _, avg = get_student_performance(s["id"])
        if "At Risk" in calculate_risk(avg):
            at_risk += 1

    # =========================
    # KPI CARDS
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            total_students,
            help="Total registered students in the system"
        )

    with col2:
        st.metric(
            "📚 Total Subjects",
            total_subjects,
            help="All subjects currently available"
        )

    with col3:
        st.metric(
            "📈 Average Score",
            avg_score if scores else "N/A",
            help="Global performance average"
        )

    with col4:
        st.metric(
            "🚨 At Risk Students",
            at_risk,
            help="Students needing immediate attention"
        )

    # =========================
    # INSIGHT SECTION
    # =========================
    st.divider()

    st.subheader("🧠 System Insight")

    if not students:
        st.info("📌 No students registered yet. Start by adding students to unlock analytics.")
    elif at_risk == 0:
        st.success("🎉 Great! No students are currently at risk.")
    elif at_risk <= 2:
        st.warning("⚠️ A few students need attention. Monitor performance closely.")
    else:
        st.error("🚨 High alert: Many students are at risk. Intervention needed!")

    # =========================
    # PERFORMANCE SNAPSHOT
    # =========================
    st.subheader("📊 Performance Snapshot")

    if scores:
        colA, colB = st.columns(2)

        with colA:
            st.info(f"📊 Total Scores Recorded: {len(scores)}")

        with colB:
            pass_rate = round((sum(1 for s in scores if s[0] >= 50) / len(scores)) * 100, 1)
            st.info(f"✅ Pass Rate (≥50): {pass_rate}%")
    else:
        st.info("No score data available yet.")

# =========================
# 👨‍🎓 STUDENTS
# =========================
elif menu == "👨‍🎓 Students":

    st.header("➕ Add New Student")

    with st.form("student_form"):
        name = st.text_input("Student Name")
        age = st.number_input("Age", 3, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        class_name = st.text_input("Class")

        submitted = st.form_submit_button("Add Student")

        if submitted:
            result = create_student(name, age, gender, class_name)
            st.success(result)

    st.header("📋 All Students")
    st.dataframe(list_students())

    st.header("🗑️ Delete Student")

    students = list_students()

    if students:
        student_map = {s["name"]: s["id"] for s in students}
        selected = st.selectbox("Select student", list(student_map.keys()))

        if st.button("Delete Student"):
            delete_student(student_map[selected])
            st.success("Deleted successfully")
            st.rerun()

# =========================
# 📚 SUBJECTS
# =========================
elif menu == "📚 Subjects":

    st.header("📚 Manage Subjects")

    with st.form("subject_form"):
        subject_name = st.text_input("Subject Name")
        submit = st.form_submit_button("Add Subject")

        if submit:
            result = add_subject(subject_name)
            st.success(result)

# =========================
# 📝 SCORES (UPGRADED UX)
# =========================
elif menu == "📝 Scores":

    st.header("📝 Score Management Center")

    # =========================
    # SESSION STATE (CONFIRMATIONS)
    # =========================
    if "score_msg" not in st.session_state:
        st.session_state.score_msg = None

    if "delete_msg" not in st.session_state:
        st.session_state.delete_msg = None

    students = list_students()
    subjects = get_all_subjects()

    if not students or not subjects:
        st.warning("Add students and subjects first.")
    else:

        student_map = {s["name"]: s["id"] for s in students}
        subject_map = {s[1]: s[0] for s in subjects}

        # =========================
        # 👤 SWITCH STUDENT
        # =========================
        selected_student = st.selectbox(
            "👤 Select Student",
            list(student_map.keys())
        )

        student_id = student_map[selected_student]

        scores, avg = get_student_performance(student_id)

        # =========================
        # ✔ SUCCESS / DELETE MESSAGES (PERSISTENT)
        # =========================
        if st.session_state.score_msg:
            st.success(st.session_state.score_msg)

        if st.session_state.delete_msg:
            st.success(st.session_state.delete_msg)

        # =========================
        # ➕ ADD SCORE FORM
        # =========================
        st.subheader("➕ Add New Score")

        with st.form("score_form"):

            selected_subject = st.selectbox(
                "Subject",
                list(subject_map.keys())
            )

            score = st.number_input("Score", 0, 100)
            date = st.date_input("Date", datetime.date.today())

            submit = st.form_submit_button("Save Score")

        # 👉 message container (RIGHT BELOW BUTTON AREA)
        score_msg = st.empty()

        if submit:

            result = record_score(
                student_id,
                subject_map[selected_subject],
                score,
                str(date)
            )

            if "successfully" in result or "scored" in result:

                score_msg.success(
                    f"✅ {selected_student} scored {score} in {selected_subject} successfully!"
                )

            else:
                score_msg.warning(result)

        # =========================
        # 📊 STUDENT DETAILS
        # =========================
        st.subheader("📊 Detailed Scores")

        if scores:

            df = pd.DataFrame(scores, columns=["ID", "Subject", "Score", "Date"])
            st.dataframe(df)

            # =========================
            # 🗑️ DELETE SCORE
            # =========================
            st.subheader("🗑️ Delete Score")

            score_map = {
                f"{row['Subject']} - {row['Score']}": row["ID"]
                for _, row in df.iterrows()
            }

            selected_score = st.selectbox(
                "Select Score",
                list(score_map.keys())
            )

            delete_msg = st.empty()

            if st.button("Delete Score"):

                score_id = score_map[selected_score]

                subject_name = selected_score.split(" - ")[0]
                score_value = selected_score.split(" - ")[1]

                delete_score(score_id)

                # ✅ SHOW CONFIRMATION (NO RERUN)
                delete_msg.success(
                    f"🗑️ Deleted: {selected_student} → {subject_name} ({score_value})"
                )
            # =========================
            # 🏆 STRONG VS WEAK SUBJECTS
            # =========================
            st.subheader("🏆 Strong vs Weak Subjects")

            subject_stats = df.groupby("Subject")["Score"].mean().reset_index()
            subject_stats = subject_stats.sort_values("Score", ascending=False)

            st.dataframe(subject_stats)

            # =========================
            # 📈 VISUAL TREND
            # =========================
            st.subheader("📈 Performance Trend")

            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date")

            df["Smoothed"] = df["Score"].rolling(2, 1).mean()

            st.line_chart(df.set_index("Date")[["Score", "Smoothed"]])

        else:
            st.info("No scores for this student yet.")

# =========================
# 📈 ANALYTICS
# =========================
elif menu == "📈 Analytics":

    st.header("📊 Analytics Dashboard")

    students = list_students()

    if students:

        student_map = {s["name"]: s["id"] for s in students}
        selected = st.selectbox("Select Student", list(student_map.keys()))

        student_id = student_map[selected]
        scores, avg = get_student_performance(student_id)
        risk = calculate_risk(avg)

        st.write("### Average Score:", avg)
        st.write("### Risk:", risk)

        insights = generate_insights(scores, avg, selected)
        st.info(insights)

        if scores:

            df = pd.DataFrame(scores, columns=["ID", "Subject", "Score", "Date"])

            st.subheader("📊 Subject Performance")
            st.bar_chart(df.groupby("Subject")["Score"].mean())

            st.subheader("📈 Trend")
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date")
            df["Smoothed"] = df["Score"].rolling(2, 1).mean()
            st.line_chart(df.set_index("Date")[["Score", "Smoothed"]])

# =========================
# 📄 REPORTS
# =========================
elif menu == "📄 Reports":

    st.header("📄 Student Report")

    students = list_students()

    student_map = {s["name"]: s["id"] for s in students}
    selected = st.selectbox("Select Student", list(student_map.keys()))

    student_id = student_map[selected]

    scores, avg = get_student_performance(student_id)
    risk = calculate_risk(avg)
    insights = generate_insights(scores, avg, selected)

    if st.button("Generate PDF"):

        file_path = generate_student_report(
            selected,
            scores,
            avg,
            risk,
            insights
        )

        with open(file_path, "rb") as f:
            pdf_bytes = f.read()

        st.write("### Preview")
        pdf_viewer(input=pdf_bytes, width=700, height=500)

        st.download_button("Download PDF", pdf_bytes, file_path, "application/pdf")

    # FULL SCHOOL REPORT
    st.subheader("📄 Full School Report")

    if st.button("Generate All Students PDF"):

        students_data = []

        for s in list_students():
            sc, av = get_student_performance(s["id"])
            rk = calculate_risk(av)
            ins = generate_insights(sc, av, s["name"])

            students_data.append({
                "name": s["name"],
                "scores": sc,
                "avg": av,
                "risk": rk,
                "insights": ins
            })

        file_path = generate_all_students_report(students_data)

        with open(file_path, "rb") as f:
            pdf_bytes = f.read()

        st.write("### Preview Full Report")
        pdf_viewer(input=pdf_bytes, width=700, height=500)

        st.download_button("Download Full Report", pdf_bytes, file_path, "application/pdf")

# =========================
# 🏆 LEADERBOARD
# =========================
elif menu == "🏆 Leaderboard":

    st.header("🏆 Top 3 Students")

    leaderboard = []

    for s in list_students():
        _, avg = get_student_performance(s["id"])
        leaderboard.append({"name": s["name"], "avg": avg})

    leaderboard = sorted(leaderboard, key=lambda x: x["avg"], reverse=True)[:3]

    for i, s in enumerate(leaderboard, 1):
        st.write(f"{i}. {s['name']} — {round(s['avg'],2)}")

# =========================
# ⚠️ ADMIN
# =========================
elif menu == "⚠️ Admin":

    st.header("⚠️ Reset System (Danger Zone)")
    st.error("🚨 WARNING: This action will permanently delete ALL data (students, scores, subjects).")

    st.write("To confirm reset, type **RESET** below:")

    confirm = st.text_input("Type RESET to confirm")

    col1, spacer, col2 = st.columns([1, 3, 1])

    # =========================
    # SESSION STATE INIT
    # =========================
    if "reset_done" not in st.session_state:
        st.session_state.reset_done = False
        st.session_state.reset_summary = None

    with col1:
        if st.button("❌ Cancel"):
            st.session_state.reset_done = False
            st.warning("Reset cancelled. No data was deleted.")

    with col2:
        if st.button("🧨 RESET ALL DATA"):

            if confirm == "RESET":

                students_count = get_student_count()
                subjects_count = get_subject_count()
                scores_count = len(get_all_scores())

                reset_database()

                # Store result in session state
                st.session_state.reset_done = True
                st.session_state.reset_summary = {
                    "students": students_count,
                    "subjects": subjects_count,
                    "scores": scores_count
                }

                st.rerun()

            else:
                st.error("❌ You must type RESET to confirm")

    # =========================
    # SHOW SUCCESS AFTER RERUN
    # =========================
    if st.session_state.reset_done:

        summary = st.session_state.reset_summary

        st.success("✅ System reset completed successfully")

        st.info(
            f"""
            📊 Reset Summary:
            - Students deleted: {summary['students']}
            - Subjects deleted: {summary['subjects']}
            - Scores deleted: {summary['scores']}
            """
        )