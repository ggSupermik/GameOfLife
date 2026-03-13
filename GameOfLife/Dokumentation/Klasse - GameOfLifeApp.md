# [[GameOfLifeApp]]

## Parametererklaerung
- [[Parameter - GameOfLifeApp.__init__.target_cols]]

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
- [[Methode - GameOfLifeApp.__init__]]
- [[Methode - GameOfLifeApp.run]]
- [[Methode - GameOfLifeApp._handle_events]]
- [[Methode - GameOfLifeApp._on_window_resized]]
- [[Methode - GameOfLifeApp._handle_resize]]
- [[Methode - GameOfLifeApp._layout_from_size]]
- [[Methode - GameOfLifeApp._rebuild_controls]]
- [[Methode - GameOfLifeApp._on_cols_change]]
- [[Methode - GameOfLifeApp._advance_simulation]]
- [[Methode - GameOfLifeApp._position_to_cell]]
- [[Methode - GameOfLifeApp._paint_cell]]
- [[Methode - GameOfLifeApp._handle_left_click]]
- [[Methode - GameOfLifeApp._toggle_running]]
- [[Methode - GameOfLifeApp._increase_speed]]
- [[Methode - GameOfLifeApp._decrease_speed]]
- [[Methode - GameOfLifeApp._draw]]

## Definiert in Datei
- [[Datei - gol app.py]]
