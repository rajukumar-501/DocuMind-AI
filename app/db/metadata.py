import os
import sqlite3

DB_PATH = os.getenv("METADATA_DB_PATH", "data/document_metadata.db")
os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            num_chunks INTEGER NOT NULL
        )
        """
    )
    return conn


def save_metadata(document_id: str, filename: str, chunks: list):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO documents (document_id, filename, num_chunks) VALUES (?, ?, ?)",
            (document_id, filename, len(chunks)),
        )


def get_all_metadata():
    with _connect() as conn:
        cursor = conn.execute(
            "SELECT document_id, filename, num_chunks FROM documents ORDER BY rowid DESC"
        )
        return [
            {"document_id": row[0], "filename": row[1], "num_chunks": row[2]}
            for row in cursor.fetchall()
        ]
