from database.queries import (
    add_score,
    get_scores_by_student,
    get_student_by_id,
    get_subject_by_id,
    score_exists
)

def record_score(student_id, subject_id, score, date):

    # Convert safely
    try:
        score = float(score)
    except:
        return "Invalid score format"

    # Validate range
    if score < 0 or score > 100:
        return "Score must be between 0 and 100"

    # Check student exists
    student = get_student_by_id(student_id)
    if not student:
        return "Student not found"

    # Check subject exists
    subject = get_subject_by_id(subject_id)
    if not subject:
        return "Subject not found"

    # Prevent duplicates
    if score_exists(student_id, subject_id):
        return f"{student[1]} already has a score in {subject[1]}"

    # Save score
    add_score(student_id, subject_id, score, date)

    return f"{student[1]} scored {score} in {subject[1]}"


def get_student_performance(student_id):
    scores = get_scores_by_student(student_id)

    if not scores:
        return [], 0

    total = sum([float(s[2]) for s in scores])  # score is index 2
    avg = total / len(scores)

    return scores, avg