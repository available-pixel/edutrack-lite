# database/db.py
# 🔌 Database connection + initialization (Streamlit Cloud safe)

import sqlite3
import os

DB_NAME = "edutrack.db"


# =========================
# CONNECTION
# =========================
def get_connection():
    """
    Create and return a SQLite connection
    Safe for Streamlit Cloud (disable thread check issues)
    """
    conn = sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )
    return conn


# =========================
# INIT DATABASE
# =========================
def init_db():
    """
    Create all tables if they don't exist
    Runs automatically on app startup
    """
    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # STUDENTS TABLE
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        class_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # SUBJECTS TABLE
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # =========================
    # SCORES TABLE
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        score REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(subject_id) REFERENCES subjects(id)
    )
    """)

    # =========================
    # NOTES TABLE
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        note TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    conn.commit()
    conn.close()