import requests
import sqlite3
from datetime import datetime, UTC

DB_NAME = "jokes.db"

def create_table():
    """Create the jokes table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jokes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_id INTEGER UNIQUE,  -- make api_id unique to prevent duplicates
        type TEXT,
        setup TEXT NOT NULL,
        punchline TEXT NOT NULL,
        fetched_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_jokes():
    """Fetch jokes from API and save at least 5 into the database."""
    url = "https://official-joke-api.appspot.com/random_ten"
    response = requests.get(url)

    if response.status_code == 200:
        jokes = response.json()
    else:
        print("Error fetching jokes:", response.status_code)
        jokes = []

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    count = 0
    for joke in jokes[:5]:  # save first 5 jokes
        try:
            cursor.execute("""
            INSERT INTO jokes (api_id, type, setup, punchline, fetched_at)
            VALUES (?, ?, ?, ?, ?)
            """, (
                joke.get("id"),
                joke.get("type"),
                joke.get("setup"),
                joke.get("punchline"),
                datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
            ))
            count += 1
        except sqlite3.IntegrityError:
            # This happens if the joke (api_id) already exists
            print(f"⚠️ Duplicate joke skipped: {joke.get('setup')}")

    conn.commit()
    conn.close()
    print(f"✅ {count} new jokes saved into {DB_NAME}")

def view_jokes():
    """Retrieve and display all saved jokes."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, setup, punchline, fetched_at FROM jokes")
    rows = cursor.fetchall()
    conn.close()

    print("\n--- Saved Jokes ---")
    for row in rows:
        print(f"[{row[0]}] ({row[1]}) {row[2]} - {row[3]} (saved at {row[4]})")

# Run everything
if __name__ == "__main__":
    create_table()
    save_jokes()
    view_jokes()


