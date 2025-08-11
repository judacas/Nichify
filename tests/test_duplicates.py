from types import SimpleNamespace
from src.spotify_handler import find_exact_duplicates


def test_find_exact_duplicates_monkeypatched(monkeypatch):
    mock_tracks = [
        {"track": {"id": "t1", "name": "Song A", "artists": [{"name": "Art"}], "duration_ms": 200000}},
        {"track": {"id": "t2", "name": "Song A", "artists": [{"name": "Art"}], "duration_ms": 200000}},
        {"track": {"id": "t3", "name": "Song B", "artists": [{"name": "Art"}], "duration_ms": 190000}},
        {"track": {"id": "t4", "name": "Song A", "artists": [{"name": "Art"}], "duration_ms": 200000}},
    ]

    def fake_get_tracks(_playlist_id: str):
        return mock_tracks

    monkeypatch.setattr("src.spotify_handler.get_all_playlist_tracks", fake_get_tracks)

    duplicates = find_exact_duplicates("dummy")
    # Only one duplicate group for Song A with same artist & duration
    assert len(duplicates) == 1
    # Ensure all duplicate ids for Song A returned
    ids = sorted(list(duplicates.values())[0])
    assert ids == ["t1", "t2", "t4"]