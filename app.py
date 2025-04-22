# Datei: /home/pi/webserver/app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta, date
import sqlite3
import os
import calendar
import requests

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'bookings.db')

FEIERTAGE_API = "https://feiertage-api.de/api/?jahr={year}&nur_land=NW"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                note TEXT
            )
        """)

def get_feiertage(year, month):
    try:
        url = FEIERTAGE_API.format(year=year)
        r = requests.get(url, timeout=5)
        data = r.json()
        result = {}
        for name, f in data.items():
            if f["datum"].startswith(f"{year}-{month:02d}"):
                result[f["datum"]] = name
        return result
    except Exception:
        return {}

def get_calendar_weeks(year, month):
    calendar_weeks = {}
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        datum = date(year, month, day)
        iso_year, iso_week, _ = datum.isocalendar()
        calendar_weeks[f"{year}-{month:02d}-{day:02d}"] = iso_week
    return calendar_weeks

@app.route('/')
@app.route('/<int:year>/<int:month>')
def index(year=None, month=None):
    today = datetime.today()
    if not year or not month:
        year = today.year
        month = today.month

    days = [(day, f"{year}-{month:02d}-{day:02d}") for day in range(1, calendar.monthrange(year, month)[1]+1)]

    bookings = {datum: [] for _, datum in days}
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT date, time, name, note FROM bookings WHERE date LIKE ?", (f"{year}-{month:02d}-%",))
        for row in cur.fetchall():
            bookings[row[0]].append({"time": row[1], "name": row[2], "note": row[3]})

    feiertage = get_feiertage(year, month)
    kalenderwochen = get_calendar_weeks(year, month)

    prev_month = (month - 1) if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = (month + 1) if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render_template('index.html', year=year, month=month, days=days, bookings=bookings,
                           feiertage=feiertage, kalenderwochen=kalenderwochen,
                           prev_year=prev_year, prev_month=prev_month,
                           next_year=next_year, next_month=next_month,
                           datetime=datetime)

@app.route('/buchen/<datum>', methods=['GET', 'POST'])
def buchen(datum):
    zeitslots = [f"{h:02d}:{m:02d}" for h in range(9, 18) for m in (0, 30)] + ["18:00"]
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        note = request.form['note']

        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO bookings (name, date, time, note) VALUES (?, ?, ?, ?)",
                         (name, datum, time, note))
        return redirect(url_for('buchen', datum=datum))

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT time FROM bookings WHERE date = ?", (datum,))
        booked = [row[0] for row in cur.fetchall()]

    return render_template('form.html', datum=datum, zeitslots=zeitslots, booked=booked)

@app.route('/api/termine/<datum>')
def api_termine(datum):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT name, time, note FROM bookings WHERE date = ? ORDER BY time", (datum,))
        entries = cur.fetchall()
    return jsonify([
        {"name": name, "time": time, "note": note} for name, time, note in entries
    ])

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5050)

