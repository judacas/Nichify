# Nichify

## Overview

Nichify enhances Spotify by introducing advanced playlist management tools. It utilizes OpenAI's GPT-4o-mini model and Spotipy to provide an intelligent, automated, and customizable playlist management experience. The project simplifies tasks like combining, splitting, filtering, and cleaning up playlists, making Spotify more intuitive and powerful for users.

---

## Features

### 1. Remove Duplicates

- Detect and remove exact duplicate tracks in playlists.
- Planned: Identify and handle similar (but not exact) duplicates.

### 2. Automation

Nichify supports:

- **On-Demand Execution**: Run commands directly via the menu-based interface.

---

## Technologies Used

- **Python**
- **Spotipy**: To interact with the Spotify Web API.
- **OpenAI GPT-4o-mini**: For AI-based decision-making and task management.
- **SQLAlchemy**: For managing a PostgreSQL database to cache metadata and user actions.

---

## File Structure

### Main Components

- `main.py`: Entry point for the application. Handles the user interface and request routing.
- `ai_handler.py`: Manages communication with OpenAI's GPT-4o-mini model.
- `ai_commands.py`: Contains specific command implementations like removing duplicates.
- `spotify_handler.py`: Interacts with Spotify for playlist operations.
- `db_setup.py`: Sets up and initializes the PostgreSQL database.
- `constants.py`: Defines reusable constants like menu prompts.

---

## How to Run

### Prerequisites

1. Python 3.8+
2. Spotify Developer Account
3. OpenAI API Key
4. PostgreSQL Database

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/nichify.git
   cd nichify
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:

   - Create a `.env` file in the root directory with the following:
     ```env
     SPOTIPY_CLIENT_ID=your_spotify_client_id
     SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
     SPOTIPY_REDIRECT_URI=your_spotify_redirect_uri
     OPENAI_API_KEY=your_openai_api_key
     DB_HOST=127.0.0.1
     DB_PORT=5432
     DB_NAME=nichify
     DB_USER=postgres
     DB_PASSWORD=your_password
     ```

4. Initialize the database:

   ```bash
   python db_setup.py
   ```

### Run the Application

```bash
python main.py
```

---

## Usage

1. **Start Nichify**:

   - Run `main.py` to begin interacting with the application.

2. **Choose a Command**:

   - Use the menu to select features like removing duplicates.

3. **Follow the Prompts**:

   - Nichify will guide you through completing your chosen tasks.

---

## Future Features

- **Combine Playlists**:
  - Merge multiple playlists with advanced options like intertwining songs or configuring ratios.
- **Separate Playlists**:
  - Split playlists into sub-playlists by attributes like BPM, genre, artist, or album.
- **Filter Tracks**:
  - Filter playlists based on attributes such as energy level, genre, or explicit content.
- **Automatic Runs**:
  - Maintain master and sub-playlists with automatic updates when changes occur.
- **Prevent Replay of Recently Heard Songs**
- **Party QR Code Playlist Submission**
- **Tagging and Auto-Tagging of Songs**
- **Playlist Creation by Tags**

---

