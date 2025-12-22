"""Persistence adapters for counts, moments, and challenges."""

from __future__ import annotations

import sqlite3
from typing import Iterable, List, Tuple


def upsert_count(
    conn: sqlite3.Connection,
    scope: str,
    prev_token: str,
    next_token: str,
    count: int,
) -> None:
    conn.execute(
        """
        INSERT INTO counts (scope, prev_token, next_token, count)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(scope, prev_token, next_token) DO UPDATE SET count=excluded.count;
        """,
        (scope, prev_token, next_token, count),
    )
    conn.commit()


def load_counts(conn: sqlite3.Connection, scope: str, prev_token: str) -> List[Tuple[str, int]]:
    cursor = conn.execute(
        "SELECT next_token, count FROM counts WHERE scope = ? AND prev_token = ?;",
        (scope, prev_token),
    )
    return list(cursor.fetchall())


def upsert_moment(
    conn: sqlite3.Connection,
    moment_id: str,
    session_id: str,
    tags: str,
    charge: float,
    is_myth: int,
    last_turn: int,
) -> None:
    conn.execute(
        """
        INSERT INTO moments (moment_id, session_id, tags, charge, is_myth, last_turn)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(moment_id) DO UPDATE SET
            session_id=excluded.session_id,
            tags=excluded.tags,
            charge=excluded.charge,
            is_myth=excluded.is_myth,
            last_turn=excluded.last_turn;
        """,
        (moment_id, session_id, tags, charge, is_myth, last_turn),
    )
    conn.commit()


def load_moments(conn: sqlite3.Connection, session_id: str) -> List[Tuple[str, str, float, int, int]]:
    cursor = conn.execute(
        "SELECT moment_id, tags, charge, is_myth, last_turn FROM moments WHERE session_id = ?;",
        (session_id,),
    )
    return list(cursor.fetchall())


def upsert_challenge(
    conn: sqlite3.Connection,
    challenge_id: str,
    session_id: str,
    status: str,
    last_updated: int,
) -> None:
    conn.execute(
        """
        INSERT INTO challenges (challenge_id, session_id, status, last_updated)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(challenge_id) DO UPDATE SET
            session_id=excluded.session_id,
            status=excluded.status,
            last_updated=excluded.last_updated;
        """,
        (challenge_id, session_id, status, last_updated),
    )
    conn.commit()


def load_challenges(conn: sqlite3.Connection, session_id: str) -> List[Tuple[str, str, int]]:
    cursor = conn.execute(
        "SELECT challenge_id, status, last_updated FROM challenges WHERE session_id = ?;",
        (session_id,),
    )
    return list(cursor.fetchall())


def prune_session(conn: sqlite3.Connection, session_id: str) -> None:
    conn.execute("DELETE FROM moments WHERE session_id = ?;", (session_id,))
    conn.execute("DELETE FROM challenges WHERE session_id = ?;", (session_id,))
    conn.commit()
