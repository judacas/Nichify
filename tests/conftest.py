import os
import pytest

def pytest_configure():
    # Set minimal env for settings to validate
    os.environ.setdefault("OPENAI_API_KEY", "test")
    os.environ.setdefault("SPOTIPY_CLIENT_ID", "test")
    os.environ.setdefault("SPOTIPY_CLIENT_SECRET", "test")
    os.environ.setdefault("SPOTIPY_REDIRECT_URI", "http://localhost/callback")

    # Ensure settings reloads with these values
    try:
        from src.settings import reload_settings

        reload_settings()
    except Exception:
        pass