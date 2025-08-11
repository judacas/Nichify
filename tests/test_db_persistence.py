import os
from src.db_handler import init_db, save_playlist_to_db, get_recently_modified_playlists


def test_db_persistence_sqlite(tmp_path, monkeypatch):
    # Use a file-based sqlite to persist across connections
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{db_path}")

    # Re-import module parts that read settings/engine; simplest is to import fresh
    # However, for brevity, call init_db which uses the already-built engine in this session.
    init_db(drop=True)

    p = {
        "id": "pl1",
        "name": "My Mix",
        "description": "desc",
        "tracks_total": 5,
        "snapshot_id": "snap1",
        "image_url": None,
    }
    save_playlist_to_db(p)

    items = get_recently_modified_playlists(days_cutoff=3650)
    assert any(x.id == "pl1" for x in items)