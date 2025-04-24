# Flask Buchungskalender – Tanzplattform Wupperbogen

Ein moderner, responsiver Buchungskalender für öffentliche Termine – ganz ohne Login.  
Ideal für Tanzstudios, Räume oder Projekte wie die **Tanzplattform Wupperbogen**.

---

## Funktionen

- Monats- & Wochenansicht
- Buchbar ohne Benutzerkonto
- Feiertage (NRW) automatisch markiert
- Notiz & Name bei Buchung
- QR-Code fürs Handy
- Mobilfähig (responsive)
- API: `/api/termine/<datum>`

---

## Projektstruktur

```bash
.
├── app.py                  # Flask-App
├── templates/              # HTML-Seiten
│   ├── index.html          # Monatsübersicht
│   ├── form.html           # Buchung
│   └── week.html           # Wochenansicht
├── static/
│   └── style.css           # Layout
├── requirements.txt
├── bookings.db             # SQLite (automatisch erzeugt)
└── README.md
```

---

## Lokales Setup

```bash
git clone https://github.com/volkere/TP_WP_PBZ_BookingCode.git
cd TP_WP_PBZ_BookingCode
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Öffne [http://localhost:5050](http://localhost:5050)

---

## API

```http
GET /api/termine/2025-04-25
```

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

## Deployment

- Raspberry Pi: systemd oder nginx reverse proxy
- GitHub Actions, Heroku: `.github/workflows/deploy.yml`
- `.gitignore`: `bookings.db`, `venv/`, `__pycache__/`

---

## Hinweise

- E-Mail erforderlich zur Bestätigung
- Keine Anmeldung nötig – öffentlich zugänglich
- Buchungen im Klartext (kein Passwort-Schutz)

---

## Autor

Team Tanzplattform des Forum Wupperbogen (VE)  
Lizenz: MIT
