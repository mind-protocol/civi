"""SQLite schema and migration runner."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Migration:
    version: int
    sql: str


MIGRATIONS: List[Migration] = [
    Migration(
        version=1,
        sql="""
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER NOT NULL
        );
        INSERT INTO schema_version (version) VALUES (1);
        CREATE TABLE IF NOT EXISTS moments (
            moment_id TEXT PRIMARY KEY,
            session_id TEXT,
            tags TEXT,
            charge REAL,
            is_myth INTEGER,
            last_turn INTEGER
        );
        CREATE TABLE IF NOT EXISTS counts (
            scope TEXT,
            prev_token TEXT,
            next_token TEXT,
            count INTEGER,
            PRIMARY KEY (scope, prev_token, next_token)
        );
        CREATE TABLE IF NOT EXISTS challenges (
            challenge_id TEXT PRIMARY KEY,
            session_id TEXT,
            status TEXT,
            last_updated INTEGER
        );
        """,
    )
]


def apply_migrations(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL);")
    row = cursor.execute("SELECT MAX(version) FROM schema_version;").fetchone()
    current_version = row[0] if row and row[0] is not None else 0
    for migration in MIGRATIONS:
        if migration.version <= current_version:
            continue
        cursor.executescript(migration.sql)
        cursor.execute("INSERT INTO schema_version (version) VALUES (?);", (migration.version,))
        current_version = migration.version
    conn.commit()
