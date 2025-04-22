# Flask Buchungskalender – Tanzplattform Wupperbogen

Dieses Projekt ist eine webbasierte Kalenderlösung, die es ermöglicht, Termine ohne Benutzerkonto zu buchen.  
Besonders geeignet für Organisationen wie Tanzstudios, Räume oder Projekte mit öffentlichen Buchungszeiten.

---

## Funktionen

- Kalenderübersicht mit Monats- und Kalenderwochenanzeige
- Anzeige gebuchter Termine mit Name & Notiz
- Feiertage (NRW) automatisch via API markiert
- Buchungen ohne Anmeldung möglich
- Buchungsformular mit QR-Code zur mobilen Nutzung
- Responsives Layout (Desktop & Mobilgeräte)
- REST-API für externe Abfragen (`/api/termine/<datum>`)

---

## Projektstruktur

```
.
├── app.py                  # Hauptserver mit Routen & Logik
├── templates/
│   ├── index.html          # Monatsübersicht
│   └── form.html           # Buchungsformular
├── static/
│   └── style.css           # Optionales CSS
├── bookings.db             # SQLite-Datenbank (beim Start erzeugt)
├── requirements.txt        # Flask + requests
└── README.md
```

---

## Setup lokal

```bash
git clone https://github.com/dein-benutzer/flask-booking.git
cd flask-booking
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Dann im Browser öffnen: [http://localhost:5000](http://localhost:5000)

---

## API

```http
GET /api/termine/<datum>
```

Antwort:

```json
[
  {
    "name": "Max",
    "time": "10:00",
    "note": "Workshop-Buchung"
  }
]
```

---

## ⚙Deployment

- Raspberry Pi: per `systemd` oder nginx reverse proxy
- GitHub/Heroku: nutze `Procfile` und `.github/workflows/deploy.yml`
- Empfohlen: `.gitignore` mit `bookings.db`, `venv/`, `__pycache__/`

---

## Hinweise

- Keine Benutzerkonten oder Zugriffsschutz
- Daten werden im Klartext gespeichert
- QR-Code zeigt direkt auf Kalender oder Buchungsseite

---

## Autor

Projektidee & Umsetzung: Team Tanzplatform des Forum Wupperbogen (VE)

Lizenz: MIT
