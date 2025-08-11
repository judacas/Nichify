from datetime import datetime, timezone, timedelta
from typing import List
from sqlalchemy.exc import IntegrityError
import os
from sqlalchemy import DateTime, create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .settings import get_settings  # type: ignore
from .spotify_handler import get_user_playlists

settings = get_settings()

# Construct the database URL
DATABASE_URL = (
    f"postgresql+psycopg://{settings.db_user}:{settings.db_password}@"
    f"{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass


class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    album = Column(String, nullable=True)
    length = Column(Integer, nullable=True)  # Length in seconds
    song_metadata = Column(JSON, nullable=True)  # Additional metadata


class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    tracks_total = Column(Integer, nullable=False)
    snapshot_id = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    last_modified = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def save_playlist_to_db(raw_playlist_data: dict):
    # sourcery skip: extract-method
    try:
        playlist_id = raw_playlist_data["id"]
        name = raw_playlist_data["name"]
        description = raw_playlist_data.get("description")
        tracks_total = raw_playlist_data["tracks_total"]
        snapshot_id = raw_playlist_data["snapshot_id"]
        image_url = raw_playlist_data.get("image_url")

        if existing_playlist := session.query(Playlist).filter_by(id=playlist_id).first():
            if existing_playlist.snapshot_id == snapshot_id:
                print(f"Playlist '{name}' already up-to-date. Skipping...")
                return
            existing_playlist.snapshot_id = snapshot_id
            existing_playlist.last_modified = datetime.now(timezone.utc)  # type: ignore
            existing_playlist.name = name
            existing_playlist.description = description
            existing_playlist.tracks_total = tracks_total
            existing_playlist.image_url = image_url

        else:
            # Add new playlist
            new_playlist = Playlist(
                id=playlist_id,
                name=name,
                description=description,
                tracks_total=tracks_total,
                snapshot_id=snapshot_id,
                image_url=image_url,
            )
            session.add(new_playlist)

        # Commit changes
        session.commit()
        print(f"Playlist '{name}' saved successfully!")

    except IntegrityError as e:
        session.rollback()
        print(f"Database integrity error: {e}")
    except Exception as e:
        session.rollback()
        print(f"Error saving playlist: {e}")


def save_playlists_to_db(playlists_data=None):
    if playlists_data is None:
        playlists_data = get_user_playlists()
    for playlist in playlists_data:
        save_playlist_to_db(playlist)


def get_recently_modified_playlists(days_cutoff: int = 30) -> list[Playlist]:
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_cutoff)

    # Fetch all playlists modified within the cutoff date
    filtered = (
        session.query(Playlist)
        .filter(Playlist.last_modified >= cutoff_date)
        .order_by(Playlist.last_modified.desc())
        .all()
    )

    return filtered


def drop_all_tables():
    try:
        Base.metadata.drop_all(engine)
        print("All tables dropped successfully!")
    except Exception as e:
        print(f"Error dropping tables: {e}")


def init_db(drop: bool = False):
    try:
        if drop:
            drop_all_tables()
        Base.metadata.create_all(engine)
        save_playlists_to_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing the database: {e}")


if __name__ == "__main__":
    import sys

    drop = len(sys.argv) > 1 and sys.argv[1] == "--drop"
    init_db(drop=drop)
    print("\n\nRecently modified playlists:")
    for playlist in get_recently_modified_playlists():
        print(playlist.name, playlist.last_modified)

