from types import SimpleNamespace
from src.ai_commands import ai_get_closest_playlist


def test_ai_get_closest_playlist_fuzzy(monkeypatch):
    playlists = [
        SimpleNamespace(id="1", name="Chill Vibes", description="Relaxing tracks", tracks_total=10),
        SimpleNamespace(id="2", name="Workout Mix", description="Energetic songs", tracks_total=15),
    ]

    monkeypatch.setattr("src.ai_commands.get_recently_modified_playlists", lambda: playlists)

    result = ai_get_closest_playlist("chill vibe")

    assert result["status"] == "success"
    assert "open.spotify.com/playlist/1" in result["playlist"]["url"]