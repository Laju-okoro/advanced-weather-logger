🌦 Advanced Weather Logger

A Python CLI application for logging and analyzing real-time weather data.
Fetch live weather 🌍, store it in a SQLite database, view logs in beautiful tables, and export data to CSV for analysis.

✨ Features

🔍 City Search → log weather by city name

📊 View Logs → latest 20 entries in a rich, color-coded table

🔎 Filter Logs → search by city or date (YYYY-MM-DD)

💾 Database Storage → SQLite backend (advanced_weather.db)

📂 Export to CSV → save logs as ADVANCED_WEATHER_LOGS.csv

🎨 Color Output → powered by Rich
 & Colorama

⚡ No API Key Needed → uses Open-Meteo API

⚙️ Installation
1. Clone the repo
git clone https://github.com/your-username/advanced-weather-logger.git
cd advanced-weather-logger

2. Install dependencies
pip install requests rich colorama prettytable

🚀 Usage

Run the script:

python advanced_weather_api.py


At startup, you’ll choose units:

TEMPERATURE (C/F) [C]:
WIND (kmh/mph) [kmh]:
PRESSURE (hPa/inHg) [hPa]:

📖 Menu Options
======== ADVANCED WEATHER LOGGER =========
1. LOG CURRENT WEATHER (DEFAULT: LAGOS)
2. LOG BY CITY NAME
3. VIEW LOGS (LATEST 20)
4. SEARCH LOGS BY CITY/DATE
5. EXPORT LOGS TO CSV
6. EXIT

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

📂 CSV Example

Open in Excel or VS Code (with Rainbow CSV plugin):

ID	CITY	LATITUDE	LONGITUDE	TEMPERATURE (°C)	WINDSPEED (km/h)	HUMIDITY (%)	PRESSURE (hPa)	DATE(UTC)
1	Lagos, Nigeria	6.5244	3.3792	25.5	13.4	92	1013.6	2025-09-26 12:53:15
2	London, UK	51.5085	-0.1257	15.0	6.4	92	1013.6	2025-09-23 10:58:44

🛠 Troubleshooting
no such table: ADVANCED_WEATHER_LOG
→ Run the script once; it auto-creates the DB.

Wrong units?
→ Restart script and choose correct display units.



📌 Notes

🌍 Powered by Open-Meteo API (no API key required).

🗂 Logs are fully portable: view in VS Code, Excel, or any CSV viewer.

🔧 Easy to extend → add precipitation, UV index, etc.