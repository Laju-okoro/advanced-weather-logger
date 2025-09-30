🌦️ Advanced Weather Logger & 😂 Joke API Saver

This repository contains two Python projects that demonstrate working with APIs, SQLite databases, and Python libraries for creating practical applications:

   1. Advanced Weather Logger → Logs real-time weather data with rich-colored tables, CSV export, and error tracking.

   2. Joke API Saver → Fetches random jokes from the Official Joke API and saves them into a SQLite database.




🌦️ Advanced Weather Logger

A Python application that fetches live weather data using the Open-Meteo API
, logs it into a SQLite database, and displays it in a colorful tabular format using Rich
 and Colorama.

There are two versions inside this project:

Basic Weather Logger → advanced_weather_api.py

Simplified Logger Example → weather.py

Both demonstrate using APIs, databases, and pretty CLI outputs.


✨ Features

✅ Fetches live weather data (temperature, windspeed, pressure, humidity, etc.)
✅ Logs data into a SQLite database (.db file auto-created)
✅ Displays logs in a rich-colored table
✅ Exports logs to CSV format for external use
✅ Handles errors gracefully with custom error logging
✅ Clean CLI menu system for easy use


📂 Project Structure
project/
│
├── advanced_weather_api.py    # main script (advanced version)
├── weather.py                 # simplified version
├── advanced_weather.db        # SQLite DB (auto-created)
├── ADVANCED_WEATHER_LOGS.csv  # exported CSV file
└── README.md                  # this file


⚡ Installation

Clone this Repository:

git clone https://github.com/Laju-okoro/advanced-weather-logger.git
cd weather-logger


Install dependencies:

pip install requests colorama rich prettytable


▶️ Usage

Run the app from your terminal:

python weather_api.py

Menu Options
========== WEATHER LOGGER APP ===========
👉 1. LOG CURRENT WEATHER
👉 2. VIEW WEATHER LOGS
👉 3. EXIT


Option 1 → Fetches and logs the current weather into the DB

Option 2 → Displays logged records in a pretty table

Option 3 → Exit the app


Table structure:

Column	Type	Description
ID	INTEGER	Auto-incremented primary key
TEMPERATURE	REAL	Logged temperature with unit
WINDSPEED	REAL	Logged windspeed with unit
DATE	TEXT	Timestamp of when data was logged


📸 Example Output
When logging weather:
✅ WEATHER LOGGED:
TEMPERATURE: 28°C, WINDSPEED: 15 km/h  AT 2025-09-26 14:45:00

When viewing logs:
🌦️ WEATHER LOGS
+----+-------------+-----------+---------------------+
| ID | TEMPERATURE | WINDSPEED | DATE                |
+----+-------------+-----------+---------------------+
| 1  | 28°C        | 15 km/h   | 2025-09-26 14:45:00 |
| 2  | 27°C        | 12 km/h   | 2025-09-26 15:00:00 |
+----+-------------+-----------+---------------------+



🚀 Usage

Run the advanced app:

python advanced_weather_api.py


At startup, you’ll choose units:

TEMPERATURE (C/F) [C]:
WIND (kmh/mph) [kmh]:
PRESSURE (hPa/inHg) [hPa]:


📖 Menu Options
======== ADVANCED WEATHER LOGGER =========
1. Log current weather (default location)
2. Log by city name
3. View logs (latest 20)
4. Search logs by city/date
5. Export logs to CSV
6. View Error Logs
7. Exit

What each option does

🔹 Option 1: Log Current Weather

Logs weather for Lagos, Nigeria.

🔹 Option 2: Log by City Name

Enter any city (e.g., London, Cairo) → fetch & log instantly.

🔹 Option 3: View Logs

Displays latest 20 logs in a table:

🌦️ WEATHER LOGS
┏━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ CITY          ┃ LATITUDE ┃ LONGITUDE┃ TEMPERATURE ┃ WINDSPEED ┃ HUMIDITY┃ PRESSURE ┃ DATE (UTC)         ┃
┡━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
┃ 19 ┃ Lagos, Nigeria┃ 6.52     ┃ 3.38     ┃ 25.5 ℃      ┃ 13.4 km/h ┃ 92%     ┃ 1013.6 hPa┃ 2025-09-26 12:53:15┃
└────┴───────────────┴──────────┴──────────┴─────────────┴───────────┴─────────┴──────────┴────────────────────┘

🔹 Option 4: Search Logs

Search logs by:

City (London)

Date (2025-09-26)

Or both together

🔹 Option 5: Export Logs to CSV

Exports all logs into ADVANCED_WEATHER_LOGS.csv.

🔹 Option 6: View Error Logs

Shows the error_log table (most recent entries first) in a Rich table.

🔹 Option 7: Exit
Close the program.


📂 Exported CSV & Viewing Tips

After selecting Export you’ll get ADVANCED_WEATHER_LOGS.csv.

Open it in Excel or VS Code with the Rainbow CSV extension for instant tabular view and RBQL queries


ID	CITY	LATITUDE	LONGITUDE	TEMPERATURE (°C)	WINDSPEED (km/h)	HUMIDITY (%)	PRESSURE (hPa)	DATE(UTC)
1	Lagos, Nigeria	6.5244	3.3792	25.5	13.4	92	1013.6	2025-09-26 12:53:15
2	London, UK	51.5085	-0.1257	15.0	6.4	92	1013.6	2025-09-23 10:58:44





🗄 Database

Logs are stored in advanced_weather.db



⚠️ Error Logging

All unexpected errors are logged into the error log table inside advanced_weather.db.

You can inspect them using DB Browser for SQLite.




📌 Notes

🌍 Powered by Open-Meteo API (no API key required).

🗂 Logs are fully portable: view in VS Code, Excel, or any CSV viewer.

🔧 Easy to extend → add precipitation, UV index, etc.

The .db and .csv files are ignored in Git (using .gitignore) to keep the repo clean.

You can reset the database by deleting advanced_weather.db — it will auto-recreate on next run.



Troubleshooting

No current_weather in API response — check your query params; correct current_weather=true.

DB missing columns — delete the .db (or run migration logic) and re-run the script to recreate the schema.

Rich markup error (closing tag) — ensure color helper returns escaped text for bad input (escape from rich.markup).

Development / Contribution

Add new features in feature branches, open PRs.

Suggested improvements: add hourly logging job, include precipitation, add a web dashboard.




# Joke Saver App 😂

A simple Python script that fetches jokes from the **[Official Joke API](https://official-joke-api.appspot.com/)** and saves them into a **SQLite database**.  
Each time you run it, at least **5 jokes** are stored (duplicates are skipped automatically).  
You can also view all jokes saved so far in your local database.

---

## 📌 Features
- Fetches **10 random jokes** from the API, saves the first 5.
- Uses **SQLite** for lightweight local storage (`jokes.db`).
- Prevents **duplicate jokes** with a unique `api_id`.
- Displays all saved jokes in the terminal with timestamps.

---

## 🛠️ Requirements
- Python 3.9+
- Libraries:
  - `requests` (for API calls)
  - `sqlite3` (built-in with Python)

---

## 🚀 Usage

1. Clone or download this project.
2. Install dependencies (if not installed already):
   ```bash
   pip install requests
Run the script:

bash
Copy code
python jokes.py


📂 Database Schema
The SQLite database (jokes.db) contains a single table:

Column	Type	Description
id	INTEGER	Primary key (auto-incremented)
api_id	INTEGER	Unique joke ID from the API
type	TEXT	Category of the joke (e.g. "general")
setup	TEXT	The question or setup of the joke
punchline	TEXT	The punchline of the joke
fetched_at	TEXT	Timestamp when the joke was saved

📖 Example Output
scss
Copy code
✅ 5 new jokes saved into jokes.db

--- Saved Jokes ---
[1] (general) Why don’t scientists trust atoms? - Because they make up everything. (saved at 2025-09-26 15:12:33)
[2] (programming) Why do programmers prefer dark mode? - Because light attracts bugs. (saved at 2025-09-26 15:12:33)


📝 Notes
If you run the script multiple times, duplicate jokes are skipped.

Database file (jokes.db) is created in the same directory as the script.

You can open the database with any SQLite viewer (e.g., DB Browser for SQLite).

📌 Future Improvements
Search jokes by keyword.

Export jokes to CSV/JSON.

Add a CLI or web interface.