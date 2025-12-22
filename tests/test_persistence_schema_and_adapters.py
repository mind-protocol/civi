import pathlib
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from persistence.sqlite_store_schema_and_migrator import apply_migrations
from persistence.store_adapters_for_counts_moments_challenges import (
    load_counts,
    load_moments,
    load_challenges,
    prune_session,
    upsert_count,
    upsert_moment,
    upsert_challenge,
)


def test_schema_and_adapters(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    apply_migrations(conn)

    upsert_count(conn, "GLOBAL", "A", "B", 2)
    counts = load_counts(conn, "GLOBAL", "A")
    assert counts == [("B", 2)]

    upsert_moment(conn, "m1", "s1", "war", 2.0, 1, 3)
    moments = load_moments(conn, "s1")
    assert moments == [("m1", "war", 2.0, 1, 3)]

    upsert_challenge(conn, "c1", "s1", "active", 5)
    challenges = load_challenges(conn, "s1")
    assert challenges == [("c1", "active", 5)]

    prune_session(conn, "s1")
    assert load_moments(conn, "s1") == []
    assert load_challenges(conn, "s1") == []
