from database.db import get_connection


# =========================
# STUDENT OPERATIONS
# =========================

def add_student(name, age, gender, class_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students (name, age, gender, class_name)
    VALUES (?, ?, ?, ?)
    """, (name, age, gender, class_name))

    conn.commit()
    conn.close()


def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()
    return students

def get_student_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    conn.close()
    return count


def get_student_by_id(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    conn.close()
    return student

def student_exists(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
    result = cursor.fetchone()

    conn.close()
    return result is not None

def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

    conn.commit()
    conn.close()


# =========================
# SUBJECT OPERATIONS
# =========================

def subject_exists(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects WHERE name = ?", (name,))
    result = cursor.fetchone()

    conn.close()
    return result is not None

def add_subject(name):
    name = name.strip().title()

    if not name:
        return "Subject name is required"

    if subject_exists(name):
        return f"{name} already exists"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO subjects (name) VALUES (?)", (name,))

    conn.commit()
    conn.close()

    return f"{name} added successfully"


def get_all_subjects():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()

    conn.close()
    return subjects

def get_subject_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM subjects")
    count = cursor.fetchone()[0]

    conn.close()
    return count

def get_subject_by_id(subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,))
    subject = cursor.fetchone()

    conn.close()
    return subject

# =========================
# DELETE SUBJECT (ADD HERE)
# =========================
def delete_subject(subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))

    conn.commit()
    conn.close()

    return "Subject deleted successfully"

def subject_has_scores(subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM scores WHERE subject_id = ?
    """, (subject_id,))

    count = cursor.fetchone()[0]
    conn.close()

    return count > 0

# =========================
# SCORE OPERATIONS
# =========================

def add_score(student_id, subject_id, score, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO scores (student_id, subject_id, score, date)
    VALUES (?, ?, ?, ?)
    """, (student_id, subject_id, score, date))

    conn.commit()
    conn.close()

def get_scores_by_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT scores.id, subjects.name, scores.score, scores.date
    FROM scores
    JOIN subjects ON scores.subject_id = subjects.id
    WHERE scores.student_id = ?
    """, (student_id,))

    results = cursor.fetchall()

    conn.close()
    return results

def get_all_scores():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM scores")
    scores = cursor.fetchall()

    conn.close()
    return scores

def delete_score(score_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM scores WHERE id = ?", (score_id,))

    conn.commit()
    conn.close()

def score_exists(student_id, subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM scores
    WHERE student_id = ? AND subject_id = ?
    """, (student_id, subject_id))

    result = cursor.fetchone()

    conn.close()
    return result is not None

# =========================
# ADMIN OPERATIONS
# =========================

def reset_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students")
    cursor.execute("DELETE FROM subjects")
    cursor.execute("DELETE FROM scores")
    cursor.execute("DELETE FROM notes")

    conn.commit()
    conn.close()