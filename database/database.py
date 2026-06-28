from pathlib import Path
import sqlite3

APP_DIR = Path.home() / ".zygn_connector"
APP_DIR.mkdir(exist_ok=True)

DB_PATH = APP_DIR / "app.db"


def initialize_database():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS remembered_users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            remember_me INTEGER DEFAULT 0,
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()

def save_email(email):
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        INSERT INTO remembered_users(email, remember_me)
        VALUES(?,1)
        ON CONFLICT(email)
        DO UPDATE SET
            remember_me=1,
            last_login=CURRENT_TIMESTAMP
    """, (email,))

    conn.commit()
    conn.close()

def get_saved_emails():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.execute("""
        SELECT email
        FROM remembered_users
        ORDER BY last_login DESC
    """)

    emails = [row[0] for row in cursor.fetchall()]
    conn.close()

    return emails

def get_connection():
    return sqlite3.connect(DB_PATH)

def delete_email(email):
    conn = get_connection()

    conn.execute(
        """
        DELETE FROM remembered_users
        WHERE email = ?
        """,
        (email,),
    )

    conn.commit()
    conn.close()