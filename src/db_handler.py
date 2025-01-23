import datetime
from typing import Optional
from sqlalchemy.exc import IntegrityError
import os
from sqlalchemy import DateTime, create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
from spotify_handler import get_user_playlists

# Load environment variables
load_dotenv(override=True)

# Retrieve database credentials from .env
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "nichify")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Construct the database URL
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
class Base(DeclarativeBase):
    pass

# Define schema
class Song(Base): 
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    album = Column(String, nullable=True)
    length = Column(Integer, nullable=True)  # Length in seconds
    song_metadata = Column(JSON, nullable=True)  # Additional metadata
    
class Playlist(Base): 
    __tablename__ = 'playlists'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description:Optional[Column] = Column(String)
    tracks_total = Column(Integer, nullable=False)
    snapshot_id = Column(String, nullable=False)
    image_url:Optional[Column] = Column(String)
    last_modified = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
def save_playlist_to_db(raw_playlist_data: dict):
    # sourcery skip: extract-method
    try:
        playlist_id = raw_playlist_data['id']
        name = raw_playlist_data['name']
        description = raw_playlist_data.get('description')
        tracks_total = raw_playlist_data["tracks_total"]
        snapshot_id = raw_playlist_data['snapshot_id']
        image_url = raw_playlist_data.get('image_url')

        if (
            existing_playlist := session.query(Playlist)
            .filter_by(id=playlist_id)
            .first()
        ):
            if existing_playlist.snapshot_id == snapshot_id:
                print(f"Playlist '{name}' already up-to-date. Skipping...")
                return
            existing_playlist.snapshot_id = snapshot_id
            existing_playlist.last_modified = datetime.datetime.now(datetime.timezone.utc) # type: ignore
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
                image_url=image_url
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

def save_playlists_to_db(playlists = None):
    if playlists is None:
        playlists = get_user_playlists()
    for playlist in playlists:
        save_playlist_to_db(playlist)
    
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

