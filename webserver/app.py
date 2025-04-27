# Datei: /home/pi/webserver/app.py

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'bookings.db')

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

@app.route('/')
def index():
    today = datetime.today()
    days = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(14)]
    return render_template('index.html', days=days)

@app.route('/buchen/<datum>', methods=['GET', 'POST'])
def buchen(datum):
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        note = request.form['note']

        try:
            stunde = int(time.split(':')[0])
            if stunde < 9 or stunde > 18:
                return "Nur Buchungen zwischen 09:00 und 18:00 Uhr erlaubt", 400
        except:
            return "Ungültiges Zeitformat", 400

        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO bookings (name, date, time, note) VALUES (?, ?, ?, ?)",
                         (name, datum, time, note))
        return redirect(url_for('termine', datum=datum))

    return render_template('form.html', datum=datum)

@app.route('/termine/<datum>')
def termine(datum):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT name, time, note FROM bookings WHERE date = ? ORDER BY time", (datum,))
        entries = cur.fetchall()
    return render_template('termine.html', datum=datum, entries=entries)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5050)
