[README.md](https://github.com/user-attachments/files/31373495/README.md)
# Conway's Game of Life

Eine interaktive Umsetzung von Conways *Game of Life* in Python mit [pygame](https://www.pygame.org/).
Das Spielfeld ist frei skalierbar, Zellen lassen sich per Maus zeichnen und die Simulations­geschwindigkeit
ist in zehn Stufen einstellbar.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![pygame](https://img.shields.io/badge/pygame-2.x-green)

---

## Inhaltsverzeichnis

- [Features](#features)
- [Installation](#installation)
- [Starten](#starten)
- [Steuerung](#steuerung)
- [Spielregeln](#spielregeln)
- [Projektstruktur](#projektstruktur)
- [Konfiguration](#konfiguration)
- [Als .exe bauen](#als-exe-bauen)
- [Dokumentation (Obsidian-Vault)](#dokumentation-obsidian-vault)
- [Legacy-Version](#legacy-version)

---

## Features

- **Torusförmiges Spielfeld** – die Ränder sind verbunden, Gleiter laufen auf der anderen Seite wieder ein
- **Zellen zeichnen mit der Maus** – Klick zum Umschalten, Ziehen mit gedrückter Taste zum Malen (nur im Pause-Modus)
- **Größenverstellbares Raster** – Slider von 10 bis 500 Spalten, Zeilenanzahl ergibt sich aus dem Fenster
- **Resizable Fenster** – das Raster passt sich live an die Fenstergröße an, vorhandene Zellen bleiben erhalten
- **10 Geschwindigkeitsstufen** – von 1 bis 50 Generationen pro Sekunde
- **Statusanzeige** – aktuelle Generation, lebende Population, Geschwindigkeit und Lauf-Status

---

## Installation

Voraussetzung ist Python 3.11 oder neuer.

```bash
# Repository klonen
git clone <repository-url>
cd GameOfLife

# Virtuelle Umgebung anlegen (empfohlen)
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS

# Abhängigkeit installieren
pip install pygame
```

> Die mitgelieferte `.vscode/settings.json` erwartet die virtuelle Umgebung unter `.venv` im Projektordner.

---

## Starten

```bash
python pygame_game_of_life.py
```

Alternativ direkt über das Paket:

```python
from gol import GameOfLifeApp

app = GameOfLifeApp(target_cols=100)
app.run()
```

Unter Windows liegt außerdem eine vorgebaute ausführbare Datei bereit:
`GameOfLife/dist/pygame_game_of_life.exe`

---

## Steuerung

### Maus

| Aktion | Wirkung |
| --- | --- |
| Linksklick auf das Raster | Zelle umschalten (lebendig ↔ tot) |
| Linke Taste gedrückt ziehen | Zellen malen (nur bei pausierter Simulation) |
| Klick auf `Start/Pause` | Simulation starten oder anhalten |
| Klick auf `Schneller +` / `Langsamer -` | Geschwindigkeitsstufe ändern |
| Slider `Zellen` ziehen | Spaltenanzahl und damit Zellgröße anpassen |

### Tastatur

| Taste | Wirkung |
| --- | --- |
| `Leertaste` | Start / Pause |
| `+` bzw. `=` (auch Numpad) | Geschwindigkeit erhöhen |
| `-` (auch Numpad) | Geschwindigkeit verringern |

Die Geschwindigkeitsstufen entsprechen 1, 2, 3, 5, 8, 12, 18, 25, 35 und 50 Schritten pro Sekunde.

---

## Spielregeln

Für jede Zelle werden die acht Nachbarn gezählt (über die Ränder hinweg umlaufend):

- Eine **lebende** Zelle mit **2 oder 3** lebenden Nachbarn überlebt.
- Eine **tote** Zelle mit **genau 3** lebenden Nachbarn wird geboren.
- In allen anderen Fällen ist die Zelle in der nächsten Generation tot.

---

## Projektstruktur

```
.
├── pygame_game_of_life.py     # Einstiegspunkt der pygame-Anwendung
├── pygame_game_of_life.spec   # PyInstaller-Spezifikation für den .exe-Build
├── gol/
│   ├── __init__.py            # Exportiert GameOfLifeApp und GameOfLifeModel
│   ├── app.py                 # Fenster, Rendering, Eingaben, Button- und Slider-Widgets
│   ├── config.py              # Farben, Größen und Grenzwerte
│   └── model.py               # Spiellogik: Raster, Nachbarzählung, Generationsschritt
├── game_of_life.py            # Ältere Konsolenversion (siehe Legacy-Version)
├── GameOfLife/
│   ├── Dokumentation/         # Obsidian-Vault mit Zettelkasten-Dokumentation
│   ├── Copilot.md             # Konventionen für die Dokumentationsnotizen
│   ├── build/ und dist/       # PyInstaller-Artefakte inkl. fertiger .exe
│   └── .obsidian/             # Obsidian-Konfiguration
└── .vscode/settings.json      # Interpreterpfad für VS Code
```

### Architektur

Die Anwendung trennt Logik und Darstellung:

- **`GameOfLifeModel`** (`gol/model.py`) hält das Raster als verschachtelte Listen und kennt nur die
  Spielregeln – `step()`, `toggle_cell()`, `resize()` und `population_count()`. Kein pygame-Bezug.
- **`GameOfLifeApp`** (`gol/app.py`) besitzt die Hauptschleife mit 60 FPS, verarbeitet Events, berechnet
  das Layout aus der Fenstergröße und zeichnet Raster, Toolbar und Statuszeile.
- **`Button`** und **`Slider`** sind einfache, selbst gezeichnete Widgets innerhalb von `gol/app.py`.

Beim Ändern der Fenstergröße oder des Sliders wird das Modell über `resize()` angepasst; bereits gesetzte
Zellen im überlappenden Bereich bleiben dabei erhalten.

---

## Konfiguration

Alle Farb- und Größenwerte liegen zentral in [`gol/config.py`](gol/config.py):

| Konstante | Standard | Bedeutung |
| --- | --- | --- |
| `DEFAULT_TARGET_COLS` | `100` | Spaltenanzahl beim Start |
| `SLIDER_MIN_COLS` / `SLIDER_MAX_COLS` | `10` / `500` | Grenzen des Zellen-Sliders |
| `MAX_GRID_COLS` / `MAX_GRID_ROWS` | `500` | Obergrenze des Rasters |
| `TOOLBAR_HEIGHT` | `110` | Höhe der Bedienleiste in Pixeln |
| `MIN_WINDOW_WIDTH` | `420` | Minimale Fensterbreite |
| `ALIVE_COLOR`, `BACKGROUND_COLOR`, … | – | Farbpalette der Oberfläche |

---

## Als .exe bauen

Der Build erfolgt mit [PyInstaller](https://pyinstaller.org/) anhand der mitgelieferten Spec-Datei:

```bash
pip install pyinstaller
pyinstaller pygame_game_of_life.spec
```

Das Ergebnis liegt anschließend unter `dist/pygame_game_of_life.exe` (Einzeldatei, ohne Konsolenfenster).

---

## Dokumentation (Obsidian-Vault)

Der Ordner `GameOfLife/` ist ein [Obsidian](https://obsidian.md/)-Vault mit einer nach Zettelkasten-Prinzip
verlinkten Dokumentation des Codes. Für jede Datei, Klasse, Methode, jeden Parameter und jedes importierte
Modul existiert eine eigene Notiz in `GameOfLife/Dokumentation/`; die Einstiegsseite ist
[`Link Library`](GameOfLife/Dokumentation/Link%20Library.md). Die zugrunde liegenden Konventionen sind in
[`Copilot.md`](GameOfLife/Copilot.md) festgehalten.

Zum Lesen den Ordner `GameOfLife/` in Obsidian als Vault öffnen – so funktionieren die `[[Wiki-Links]]`
und die Graphansicht.

---

## Legacy-Version

`game_of_life.py` ist die ursprüngliche, textbasierte Fassung: Sie erzeugt ein zufällig gefülltes Raster
und gibt jede Runde als Zahlenlisten auf der Konsole aus. Sie ist eigenständig, nutzt kein pygame und wird
nicht mehr weiterentwickelt – die aktuelle Version ist das `gol`-Paket. Die Datei `game_of_life.txt`
enthält eine nahezu identische Sicherungskopie dieses Skripts.

```bash
python game_of_life.py
```
