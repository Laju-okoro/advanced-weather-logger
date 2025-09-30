import requests
import sqlite3
import csv
from datetime import datetime, UTC
from prettytable import PrettyTable
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.markup import escape
from typing import Optional, Union
import time

console = Console()

DB_PATH = "advanced_weather.db"
DEFAULT_LAT = 6.5244
DEFAULT_LON = 3.3792
DEFAULT_CITY = "Lagos, Nigeria"

TEMP_UNIT = "C"
WIND_UNIT = "kmh"
PRESSURE_UNIT = "hPa"


#===============================
# CONVERSION HELPERS
#===============================
def temp_to_display(raw_c: Optional[float]) -> Optional[float]:
    if raw_c is None:
        return None
    if TEMP_UNIT.upper() == "F":
        return raw_c * 9.0/5.0 + 32.0
    return raw_c

def wind_to_display(raw_kmh: Optional[float]) -> Optional[float]:
    if raw_kmh is None:
        return None
    if WIND_UNIT.lower() == "mph":
        return raw_kmh * 0.621371
    return raw_kmh

def pressure_to_display(raw_hpa: Optional[float]) -> Optional[float]:
    if raw_hpa is None:
       return None
    if PRESSURE_UNIT.lower() == "inhg":
       return raw_hpa *  0.029529983071445
    return raw_hpa

#-----------------------------------------
# NUMERIC ONLY VERSIONS FOR CSV EXPORT
#-----------------------------------------
def temp_to_display_num(raw_c: Optional[float]) ->  Union[float, str]:
    v = temp_to_display(raw_c)
    return "" if v is None else round(v, 2)

def wind_to_display_num(raw_kmh: Optional[float]) -> Union[float, str]:
    v = wind_to_display(raw_kmh)
    return "" if v is None else round(v, 2)

def pressure_to_display_num(raw_hpa: Optional[float]) -> Union[float, str]:
    v = pressure_to_display(raw_hpa)
    return "" if v is None else round(v, 2)


#-----------------------------------------------------------------
# RICH FORMAT HELPERS (CHOOSE COLOR BY RAW METRIC THRESHOLDS)
#-----------------------------------------------------------------
def format_temp(raw_c: Optional[float]) -> str:
    if raw_c is None:
        return "[yellow]N/A[/yellow]"
    try:
        if raw_c >= 30:
            color = "red"
        elif raw_c <= 10:
            color = "blue"
        else:
            color = "yellow"
        val = temp_to_display(raw_c)
        unit = "℉" if TEMP_UNIT.upper() == "F" else "℃"
        return f"[{color}]{val:.1f}{unit}[/{color}]"
    except Exception:
        return escape(str(raw_c))
    
def format_wind(raw_kmh: Optional[float]) -> str:
    if raw_kmh is None:
        return "[yellow]N/A[/yellow]"
    try:
        if raw_kmh >= 50:
            color = "red"
        elif raw_kmh >= 20:
            color = "yellow"
        else:
            color = "green"
        val = wind_to_display(raw_kmh)
        unit = "mph" if WIND_UNIT.lower() == "mph" else "km/h"
        return f"[{color}]{val:.1f} {unit}[/{color}]"
    except Exception:
        return escape(str(raw_kmh))

def format_humidity(raw_h: Optional[float]) -> str:
    if raw_h is None:
        return "[yellow]N/A[/yellow]"
    try:
        print("DEBUG humidity value:", repr(raw_h))
        return f"[green]{raw_h:.0f}%[/green]"
    except Exception:
        return escape(str(raw_h))

def format_pressure(raw_hpa: Optional[float]) -> str:
    if raw_hpa is None:
        return "[yellow]N/A[/yellow]"
    try:
        val = pressure_to_display(raw_hpa)
        unit = "inHg" if PRESSURE_UNIT.lower() == "inhg" else "hPa"
        return f"[cyan]{val:.1f} {unit}[/cyan]"
    except Exception:
        return escape(str(raw_hpa))


#============================
# CREATE DATABASE AND TABLE
#============================
def init_db():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS ADVANCED_WEATHER_LOG (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CITY TEXT,
                    LATITUDE REAL,
                    LONGITUDE REAL,
                    TEMPERATURE REAL,
                    WINDSPEED REAL,
                    HUMIDITY REAL,
                    PRESSURE REAL,
                    DATE TEXT
        )
        """)
        conn.commit()

#------------------------------
# TABLE TO LOG ERRORS
#------------------------------
        cur.execute("""
        CREATE TABLE IF NOT EXISTS ERROR_LOG(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            WHEN_TS TEXT,
            CONTEXT TEXT,
            MESSAGE TEXT        
        )
        """)
        conn.commit()

    except sqlite3.Error as e:
        print(Fore.RED + f"⚠️ DATABASE INITIALIZATION ERROR: {e}")
    finally:
        if conn:
            conn.close()


#==================================================
# GEOCODE CITY -- LAT/LON (OPEN-METEO GEOCODING)
#==================================================

def  geocode_city(city_name: str):
    """
    Returns (name, latitude, longitude) or (None, None, None) on error.
    Uses Open-Meteo geocoding API (no API key).
    """
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?"
        params = {"name": city_name, "count":1, "language": "en", "format": "json"}
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results")
        if not results:
            print(Fore.YELLOW + f"⚠️ GEOCODING: NO RESULTS FOR '{city_name}'")
            return None, None, None
        first = results[0]
        return first.get("name"), first.get("latitude"), first.get("longitude")
    except requests.RequestException as e:
        print(Fore.RED + f"⚠️ GEOCODING NETWORK ERROR: {e}")
        return None, None, None
    except Exception as e:
        print(Fore.RED + f"⚠️ GEOCODING ERROR: {e}")
        return None, None, None
    


# =====================================================================
# Fetch weather (Open-Meteo)
# - requests current_weather & hourly humidity/pressure arrays
# - find index matching current time to extract humidity & pressure
# =====================================================================
def fetch_weather(latitude=DEFAULT_LAT, longitude=DEFAULT_LON):
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
            "hourly": "relativehumidity_2m,pressure_msl",
            "timezone": "UTC"
        }
        with console.status("[bold blue]Fetching Weather...[/bold blue]", spinner="dots"):
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        

        current = data.get("current_weather")
        if not current:
            print(Fore.YELLOW + "⚠️ NO CURRENT_WEATHER IN API RESPONSE.")
            return None
        
        result = {
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "time": current.get("time")
        }

#-----------------------------------------------------------------------------
# TRY TO FETCH HUMIDITY AND PRESSURE FROM HOURLY ARRAYS BY MATCHING TIME
#-----------------------------------------------------------------------------
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        humidity_arr = hourly.get("relativehumidity_2m")
        pressure_arr = hourly.get("pressure_msl")

        if humidity_arr and pressure_arr and result["time"] in times:
            idx = times.index(result["time"])
            result["humidity"] = humidity_arr[idx]
            result["pressure"] = pressure_arr[idx]
        else:
            result["humidity"] = None
            result["pressure"] = None

        return result
    
    except requests.RequestException as e:
        print(Fore.RED + f"⚠️ WEATHER FETCH NETWORK ERROR: {e}")
    except Exception as e:
        print(Fore.RED + f"⚠️ WEATHER FETCH ERROR: {e}")
        return None
    

#==================================
# LOGGING WEATHER TO DATABASE
#===================================
def log_weather(city: Optional[str] = None, latitude: Optional[float] = None, longitude: Optional[float] = None):
     """
    Main logger. If city provided but no coords -> geocode.
    If none provided -> use DEFAULT coords.
    """
     try:
         chosen_city = city
         lat = latitude
         lon = longitude

         if city and (latitude is None or longitude is None):
             chosen_city, g_lat, g_lon = geocode_city(city)
             if g_lat is None or g_lon is None:
                 print(Fore.RED + "❌ COULD NOT GEOCODE CITY: ABORTING LOG.")
                 return
             lat = g_lat
             lon = g_lon

         if lat is None or lon is None:
             lat = DEFAULT_LAT
             lon = DEFAULT_LON
             if not chosen_city:
                chosen_city = DEFAULT_CITY

         weather = fetch_weather(lat, lon)
         if not weather:
             print(Fore.RED + "❌ COULD NOT FETCH WEATHER: NOT LOGGED.")
             return
         
         now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
         conn = sqlite3.connect(DB_PATH)
         cur = conn.cursor()
         cur.execute("""
            INSERT INTO ADVANCED_WEATHER_LOG
            (CITY, LATITUDE, LONGITUDE, TEMPERATURE, WINDSPEED, HUMIDITY, PRESSURE, DATE)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            chosen_city,
            lat,
            lon,
            weather["temperature"],
            weather["windspeed"],
            weather["humidity"],
            weather["pressure"],
            now

        ))
         conn.commit()
         city_display = escape(str(chosen_city)) if chosen_city is not None else "unknown"
         console.print(
            f"✅ WEATHER LOGGED {chosen_city}:\n "      
            f"TEMPERATURE: {format_temp(weather['temperature'])}, "  
            f"WINDSPEED: {format_wind(weather['windspeed'])}, "
            f"HUMIDITY: {format_humidity(weather['humidity'])}, "
            f"PRESSURE: {format_pressure(weather['pressure'])}, "
            f"AT: {escape(str(now))} (UTC)",
            style="bold green"
         )
     except sqlite3.Error as e:
         print(Fore.RED + f"⚠️ DATABASE ERROR WHILE LOGGING: {e}")
         log_error("log_weather", str(e))
     except Exception as e:
        print(f"DEBUG: Unexpected error caught -- {e}")
        print(Fore.RED + f"⚠️ UNEXPECTED ERROR WHILE LOGGING: {e}")
        log_error("log_weather_unexpected", str(e))

     finally:
         try:
             conn.close()
         except:
             pass

#===========================
# VIEW LOGS
#============================
def view_logs(limit: Optional[int] = None, search_city: Optional[str] = None, search_date: Optional[str] = None):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        sql = "SELECT ID, CITY, LATITUDE, LONGITUDE, TEMPERATURE, WINDSPEED, HUMIDITY, PRESSURE, DATE FROM ADVANCED_WEATHER_LOG WHERE 1=1"
        params = []
        if search_city:
            sql += " AND CITY LIKE ?"
            params.append(f"%{search_city}%")
        if search_date:
            sql += " AND DATE LIKE ?"
            params.append(f"{search_date}%")
        sql += " ORDER BY ID DESC"
        if limit:
            sql += f" LIMIT {int(limit)}"
        cur.execute(sql, params)
        rows = cur.fetchall()
        for i, row in enumerate(rows[:5]):
            print("DEBUG row sample:", i, repr(row))
        if not rows:
            console.print("\n📭 [bold yellow]NO WEATHER LOGS YET.[/]")
            return
        
        table = Table(title="🌦️ WEATHER LOGS", header_style="bold magenta", show_lines=True)
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("CITY", style="bold white")
        table.add_column("LATITUDE", style="white")
        table.add_column("LONGITUDE", style="white")
        table.add_column(f"TEMPERATURE", style="white")
        table.add_column(f"WINDSPEED", style="white")
        table.add_column("HUMIDITY", style="white")
        table.add_column("PRESSURE", style="white")
        table.add_column("DATE (UTC)", style="green")

        for r in rows:
            _id, city, lat, lon, temp, wind, hum, pres, dt = r
            city_display = escape(str(city)) if city is not None else ""
            date_display = escape(str(dt))
            table.add_row(
                str(_id),
                city_display,
                f"{lat:.2f}" if lat is not None else "N/A",
                f"{lon:.2f}" if lon is not None else "N/A",
                format_temp(temp),
                format_wind(wind),
                format_humidity(hum),
                format_pressure(pres),
                date_display
            )
        console.print(table)


    except sqlite3.Error as e:
        console.print(f"⚠️ [red]DATABASE READ ERROR:[/] {e}")
    finally:
        try:
            conn.close()
        except Exception:
            pass

#===================
# EXPORT TO CSV
#===================
def export_to_csv(filepath: str = "ADVANCED_WEATHER_LOGS.csv"):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT ID, CITY, LATITUDE, LONGITUDE, TEMPERATURE, WINDSPEED, HUMIDITY, PRESSURE, DATE FROM ADVANCED_WEATHER_LOG ORDER BY ID")
        rows = cur.fetchall()
        if not rows:
            print(Fore.YELLOW + "📭 NO LOGS TO EXPORT.")
            return
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            header = [
                "ID", "City", "Latitude", "Longitude",
                f"TEMPERATURE ({'°F' if TEMP_UNIT.upper()=='F' else '°C'})",
                f"WINDSPEED ({'mph' if WIND_UNIT.lower()=='mph' else 'km/h'})",
                "HUMIDITY (%)",
                f"PRESSURE ({'inHg' if PRESSURE_UNIT.lower()=='inhg' else 'hPa'})",
                "DATE (UTC)"
            ]

            writer.writerow(["ID", "CITY", "LATITUDE", "LONGITUDE", "TEMPERATURE", "WINDSPEED", "HUMIDITY", "PRESSURE", "DATE (UTC)"])
            writer.writerow(header)
            for r in rows:
                _id, city, lat, lon, temp, wind, hum, pres, dt = r
                writer.writerow([
                    _id,
                    city,
                    round(lat, 6) if lat is not None else "",
                    round(lon, 6) if lon is not None else "",
                    temp_to_display_num(temp),
                    wind_to_display_num(wind),
                    "" if hum is None else round(hum, 1),
                    pressure_to_display_num(pres),
                    dt
                ])
        print(Fore.GREEN + f"📂 EXPORTED {len(rows)} rows to {filepath}")
    except Exception as e:
        print(Fore.RED + f"⚠️ CSV EXPORT ERROR: {e}")
    finally:
        try:
            conn.close()
        except Exception:
            pass


#==================================
# ERROR LOGGING HELPER
#==================================
def log_error(context, message):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO ERROR_LOG (WHEN_TS, CONTEXT, MESSAGE) VALUES (?, ?, ?)",
                    (datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"), context, message))
        conn.commit()
    except Exception:
        pass
    finally:
        try:
            conn.close()
        except Exception:
            pass

#===============
# CLI MENU
#===============
def main():
    global TEMP_UNIT, WIND_UNIT, PRESSURE_UNIT
    init_db()
    console.print("[bold cyan]CHOOSE DISPLAY UNITS (PRESS ENTER TO USE DEFAULTS)[/bold cyan]")
    t = input("TEMPERATURE (C/F) [C]: ").strip().upper() or "C"
    TEMP_UNIT = "F" if t == "F" else "C"
    w = input("WIND (kmh/mph) [kmh]: ").strip().lower() or "kmh"
    WIND_UNIT = "mph" if w == "mph" else "kmh"
    p = input("PRESSURE (hPa/inHg) [hPa]: ").strip().lower() or "hPa"
    PRESSURE_UNIT = "inHg" if p == "inHg" else "hPa"
    
    while True:
        console.print("\n[bold cyan]======== ADVANCED WEATHER LOGGER =========[/]")
        console.print("1. LOG CURRENT WEATHER (DEFAULT LOCATION: LAGOS)")
        console.print("2. LOG BY CITY NAME")
        console.print("3. VIEW LOGS (LATEST 20)")
        console.print("4. SEARCH LOGS BY CITY/DATE")
        console.print("5. EXPORT LOGS TO CSV")
        console.print("6. EXIT")
    
        choice = input(Fore.CYAN + "CHOOSE AN OPTION (1-6): ").strip()

        if choice == "1":
            with console.status("[bold green]Fetching Weather...[/]", spinner="earth"):
                time.sleep(1)
                log_weather() 

        elif choice == "2":
            city = input(Fore.BLUE + "CITY NAME (LONDON, CAIRO): ").strip()
            if city:
                with console.status("[bold green]Fetching Weather...[/]", spinner="earth"):
                      time.sleep(1)
                      log_weather(city=city)     

        elif choice == "3":
            view_logs(limit=20)

        elif choice == "4":
            city = Prompt.ask("🔍 ENTER CITY (OR LEAVE BLANK)", default="")
            date = Prompt.ask("📅 ENTER DATE (YYYY-MM-DD OR BLANK)", default="")
            view_logs(search_city=city, search_date= date)

        elif choice == "5":
            export_to_csv()

        elif choice == "6":
            console.print("👋 GOODBYE", style="bold red")
            break
        else:
            print(Fore.YELLOW + "❌ INVALID CHOICE")


if __name__ == "__main__":
    main()
