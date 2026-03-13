# [[GameOfLifeApp]]

## Parametererklaerung
- [[Parameter - GameOfLifeApp.__init__.target_cols.md]]

## Globale Variablen der Klasse
- `window`: Pygame-Fenster.
- `target_cols`: Soll-Breite des Grids in Zellen (via Slider einstellbar).
- `cell_size`: Dynamisch berechnete Zellkantenlaenge in Pixeln.
- `font`, `small_font`: Schriftobjekte.
- `running`: Simulationsstatus.
- `speed_level`: Geschwindigkeitsstufe 1-10.
- `_time_accumulator`: Zeitpuffer fuer Schrittsteuerung.
- `_last_grid_rect`: Zuletzt gerenderter Gridbereich.
- `model`: Instanz von [[GameOfLifeModel]].
- `buttons`: Liste von [[Button]]-Objekten.
- `slider`: Optionale Instanz von [[Slider]].

## Methoden
- [[Methode - GameOfLifeApp.__init__.md]]
- [[Methode - GameOfLifeApp.run.md]]
- [[Methode - GameOfLifeApp._handle_events.md]]
- [[Methode - GameOfLifeApp._on_window_resized.md]]
- [[Methode - GameOfLifeApp._handle_resize.md]]
- [[Methode - GameOfLifeApp._layout_from_size.md]]
- [[Methode - GameOfLifeApp._rebuild_controls.md]]
- [[Methode - GameOfLifeApp._on_cols_change.md]]
- [[Methode - GameOfLifeApp._advance_simulation.md]]
- [[Methode - GameOfLifeApp._position_to_cell.md]]
- [[Methode - GameOfLifeApp._paint_cell.md]]
- [[Methode - GameOfLifeApp._handle_left_click.md]]
- [[Methode - GameOfLifeApp._toggle_running.md]]
- [[Methode - GameOfLifeApp._increase_speed.md]]
- [[Methode - GameOfLifeApp._decrease_speed.md]]
- [[Methode - GameOfLifeApp._draw.md]]

## Definiert in Datei
- [[Datei - gol app.py.md]]
