import requests
import sqlite3
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table

# INITIALIZING COLORAMA AND RICH
init(autoreset=True)
console = Console()

# 1. Connect to database and Create table
def init_db():
    try:

        conn = sqlite3.connect("weather.db")
        cursor = conn.cursor()

        # Create table if it does not exist

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS WEATHER_LOG (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TEMPERATURE REAL,
            WINDSPEED REAL,
            DATE TEXT
        )    
        """)
        conn.commit()
        print(Fore.GREEN + "✅ DATABASE INITIALIZED SUCCESSFULLY.")
    except sqlite3.Error as e:
        print(Fore.RED + f"⚠️ DATABASE ERROR WHILE READING LOGS: {e}")


# Fetch live weather API data
url = "https://api.open-meteo.com/v1/forecast?latitude=9.08&longitude=8.68&current_weather=true"
response = requests.get(url)

if response.status_code == 200:
    weather_data = response.json()
    selected_data = weather_data['current_weather']
    units = weather_data['current_weather_units']
    temp = f'{selected_data['temperature']}{units['temperature']}'
    windspeed = f'{selected_data['windspeed']}{units['windspeed']}'

else:
    print(Fore.RED + "⚠️FAILED TO FETCH WEATHER DATA!!")


def log_weather():
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect("weather.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO WEATHER_LOG (TEMPERATURE, WINDSPEED, DATE) VALUES(?, ?, ?)",
                   (temp, windspeed, now))
        conn.commit()
        print(Fore.CYAN + f'✅ WEATHER LOGGED:\n'
              + Fore.YELLOW + f"TEMPERATURE: {temp}"
              + Fore.CYAN + ","
               + Fore.YELLOW +  f" WINDSPEED: {windspeed} "
               + Fore.CYAN + f" AT {now}")

    except sqlite3.Error as e:
        print(Fore.RED + f"⚠️ DATABASE ERROR WHILE READING LOGS: {e}")



#  View all records
def view_logs():
    try:
        conn = sqlite3.connect("weather.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM WEATHER_LOG")
        rows = cursor.fetchall()

        if not rows:
            print(Fore.YELLOW + "\n📭 NO WEATHER LOGS FOUND.")

        else:
            table = Table(title="🌦️ WEATHER LOGS", style="bold magenta")
            table.add_column("ID", justify="center", style="cyan", no_wrap=True)
            table.add_column("TEMPERATURE", justify="center", style="yellow", no_wrap=False, overflow="fold")
            table.add_column("WINDSPEED", justify="center", style="blue", no_wrap=False, overflow="fold")
            table.add_column("DATE", justify="center", style="green", no_wrap=False, overflow="fold")
            
            for row in rows:
                table.add_row(
                    str(row[0]),
                    f"{row[1]}",
                    f"{row[2]}",
                    row[3]
                )

            console.print(table)
    except sqlite3.Error as e:
        print(Fore.RED + f"⚠️ DATABASE ERROR WHILE READING LOGS: {e}")
    finally:
        conn.close()



# Main Menu
def main():
    init_db()
    while True:
        print(Fore.MAGENTA + '\n========== WEATHER LOGGER APP ===========')
        print(Fore.GREEN + "👉 1. LOG CURRENT WEATHER")
        print(Fore.GREEN + "👉 2. VIEW WEATHER LOGS")
        print(Fore.GREEN + "👉 3. EXIT")
        choice = input(Fore.YELLOW + 'CHOOSE AN OPTION (1-3): ' + Style.RESET_ALL)

        if choice == '1':
            log_weather()

        elif choice == '2':
            view_logs()

        elif choice == '3':
            print(Fore.MAGENTA + "EXITING THE WEATHER APP\n👋 GOODBYE!!")
            break
        else:
            print(Fore.RED + "❌ INVALID CHOICE\nTRY AGAIN!!")

if __name__ == "__main__":
    main()
