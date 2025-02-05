import sqlite3
from typing import Optional
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class Candidate:
    id: int
    job_profile: str
    name: str
    email: str
    phone: str
    

class DatabaseDriver:
    def __init__(self, db_path: str = "interview_db.sqlite"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Create cars table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_profile TEXT NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL
                )
            """)
            conn.commit()

    def create_candidate(self, job_profile: str, name: str,email: str, phone: str) -> Candidate:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO AUTOINCREMENT (job_profile, name, email, phone) VALUES (?, ?, ?, ?)",
                (job_profile, name, email, phone)
            )
            conn.commit()
            return Candidate(job_profile=job_profile,name=name,email=email,phone=phone)

    def get_candidate_by_email(self, email: str) -> Optional[Candidate]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM candidates WHERE email = ?", (email))
            row = cursor.fetchone()
            if not row:
                return None
            
            return Candidate(
                id=row[0],
                job_profile=row[1],
                name=row[2],
                email=row[3],
                phone=row[4]
            )