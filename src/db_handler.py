from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from typing import Iterator, List
from sqlalchemy.exc import IntegrityError
import os
from sqlalchemy import DateTime, create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session as SASession
from .settings import get_settings  # type: ignore
from .spotify_handler import get_user_playlists
import logging

logger = logging.getLogger(__name__)

settings = get_settings()

# Construct the database URL (allow DATABASE_URL override)
DATABASE_URL = settings.database_url or (
    f"postgresql+psycopg://{settings.db_user}:{settings.db_password}@"
    f"{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def get_session() -> Iterator[SASession]:
    session = SessionFactory()
    try:
        yield session
        session.close()
    except Exception:
        session.close()
        raise


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
    try:
        playlist_id = raw_playlist_data["id"]
        name = raw_playlist_data["name"]
        description = raw_playlist_data.get("description")
        tracks_total = raw_playlist_data["tracks_total"]
        snapshot_id = raw_playlist_data["snapshot_id"]
        image_url = raw_playlist_data.get("image_url")

        with get_session() as session:
            if existing_playlist := session.query(Playlist).filter_by(id=playlist_id).first():
                if existing_playlist.snapshot_id == snapshot_id:
                    logger.info("Playlist '%s' already up-to-date. Skipping...", name)
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

            session.commit()
            logger.info("Playlist '%s' saved successfully!", name)

    except IntegrityError as e:
        logger.error("Database integrity error: %s", e)
    except Exception:
        logger.exception("Error saving playlist")


def save_playlists_to_db(playlists_data=None):
    if playlists_data is None:
        playlists_data = get_user_playlists()
    for playlist in playlists_data:
        save_playlist_to_db(playlist)


def get_recently_modified_playlists(days_cutoff: int = 30) -> list[Playlist]:
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_cutoff)

    with get_session() as session:
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
        logger.info("All tables dropped successfully!")
    except Exception:
        logger.exception("Error dropping tables")


def init_db(drop: bool = False):
    try:
        if drop:
            drop_all_tables()
        Base.metadata.create_all(engine)
        save_playlists_to_db()
        logger.info("Database initialized successfully!")
    except Exception:
        logger.exception("Error initializing the database")


if __name__ == "__main__":
    import sys

    drop = len(sys.argv) > 1 and sys.argv[1] == "--drop"
    init_db(drop=drop)
    print("\n\nRecently modified playlists:")
    for playlist in get_recently_modified_playlists():
        print(playlist.name, playlist.last_modified)

