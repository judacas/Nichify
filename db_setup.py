import os
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

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
Base = declarative_base()

# Define schema
class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    album = Column(String, nullable=True)
    length = Column(Integer, nullable=True)  # Length in seconds
    song_metadata = Column(JSON, nullable=True)  # Additional metadata

class UserAction(Base):
    __tablename__ = 'user_actions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)  # ISO 8601 format

# Create tables
def init_db():
    try:
        Base.metadata.create_all(engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Failed to create tables: {e}")

if __name__ == "__main__":
    init_db()
