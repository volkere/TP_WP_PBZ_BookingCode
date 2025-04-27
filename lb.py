import pygame
import sys
import os
import math
import time
import urllib.request

# Initialisierung
pygame.init()

# Fenstergröße
window_width, window_height = 800, 200  # Extra Platz für QR-Code
screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)

# MacOS: Fenster nach vorne holen
if sys.platform == "darwin":
    os.system("""osascript -e 'tell application "System Events" to set frontmost of the first process whose unix id is (do shell script "echo $PPID") to true'""")

# Schrift
font = pygame.font.SysFont(None, 50)

# Farben erzeugen (Regenbogen)
def rainbow_color(tick):
    r = int((math.sin(tick * 0.05) + 1) * 127)
    g = int((math.sin(tick * 0.05 + 2) + 1) * 127)
    b = int((math.sin(tick * 0.05 + 4) + 1) * 127)
    return (r, g, b)

# Nachrichten laden
def lade_nachrichten(dateiname):
    try:
        with open(dateiname, "r", encoding="utf-8") as f:
            nachrichten = [zeile.strip() for zeile in f if zeile.strip()]
            if not nachrichten:
                nachrichten = ["Keine Nachrichten vorhanden."]
            return nachrichten
    except FileNotFoundError:
        return ["Datei 'nachrichten.txt' nicht gefunden!"]

# Nachrichtenliste
skript_verzeichnis = os.path.dirname(os.path.abspath(__file__))
nachrichten_pfad = os.path.join(skript_verzeichnis, "nachrichten.txt")
nachrichten = lade_nachrichten(nachrichten_pfad)
nachrichten_index = 0
aktuelle_nachricht = nachrichten[nachrichten_index]

# QR-Code herunterladen
qr_url = "https://api.qrserver.com/v1/create-qr-code/?data=http://ca09-2a02-908-f62-61e0-e1a7-e4b1-6c71-f01e.ngrok-free.app/&size=160x160"
qr_image_path = os.path.join(skript_verzeichnis, "qr_code.png")
urllib.request.urlretrieve(qr_url, qr_image_path)
qr_image = pygame.image.load(qr_image_path)

# Text vorbereiten
def erstelle_text_surface(text, farbe):
    surface = font.render(text, True, farbe)
    rect = surface.get_rect(center=(window_width // 2, window_height // 2))
    return surface, rect

# Anfangswerte
x = window_width
tick = 0
nachricht_wechsel_intervall = 20  # Sekunden
letzter_nachricht_wechsel = time.time()

# Hauptschleife
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hintergrund
    screen.fill((0, 0, 0))

    # QR-Code anzeigen
    screen.blit(qr_image, (window_width - 180, 20))  # Rechts oben platzieren

    # Regenbogenfarbe berechnen
    current_color = rainbow_color(tick)
    text_surface, text_rect = erstelle_text_surface(aktuelle_nachricht, current_color)

    # Text verschieben
    x -= 2
    if x < -text_rect.width:
        x = window_width

    screen.blit(text_surface, (x, window_height // 2 - text_rect.height // 2))
    pygame.display.update()
    clock.tick(60)
    tick += 1

    # Nachrichtenwechsel nach Intervall
    if time.time() - letzter_nachricht_wechsel > nachricht_wechsel_intervall:
        nachrichten_index = (nachrichten_index + 1) % len(nachrichten)
        aktuelle_nachricht = nachrichten[nachrichten_index]
        x = window_width
        letzter_nachricht_wechsel = time.time()

pygame.quit()
sys.exit()

