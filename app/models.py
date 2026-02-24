import json

from app.database import get_db_connection

DEFAULT_STUDENT_SKILLS = {
    "tenses": 50,
    "articles": 50,
    "prepositions": 50,
    "subject_verb_agreement": 50,
    "modals": 50,
    "conditionals": 50,
    "active_passive": 50,
    "direct_indirect": 50,
    "conjunctions": 50,
    "error_correction": 50,
}


def create_user(email, password, role, grade=None):
    skills = json.dumps(DEFAULT_STUDENT_SKILLS) if role == "student" else json.dumps({})

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (email, password, role, grade, skills)
        VALUES (?, ?, ?, ?, ?)
        """,
        (email, password, role, grade, skills),
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_all_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role = 'student'")
    students = cursor.fetchall()
    conn.close()
    return students


def update_user_skills(email, skills_json):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET skills = ? WHERE email = ?",
        (skills_json, email),
    )
    conn.commit()
    conn.close()

    main
    )
    conn.commit()
    conn.close()
