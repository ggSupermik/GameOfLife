# [[Slider]]

## Parametererklaerung
- [[Parameter - Slider.__init__.rect]]
- [[Parameter - Slider.__init__.min_val]]
- [[Parameter - Slider.__init__.max_val]]
- [[Parameter - Slider.__init__.value]]
- [[Parameter - Slider.__init__.label]]
- [[Parameter - Slider.__init__.on_change]]

## Globale Variablen der Klasse
- `TRACK_H`: Hoehe der Slider-Track-Darstellung.
- `THUMB_R`: Radius des Slider-Knaufs.
- `rect`: Zeichen- und Interaktionsbereich.
- `min_val`, `max_val`, `value`: Wertebereich und aktueller Wert.
- `label`: Beschriftung links vom Slider.
- `on_change`: Callback bei Wertaenderung.
- `_dragging`: Interner Drag-Status.

## Methoden
- [[Methode - Slider.__init__]]
- [[Methode - Slider.thumb_x]]
- [[Methode - Slider._apply_x]]
- [[Methode - Slider.handle_mousedown]]
- [[Methode - Slider.handle_mouseup]]
- [[Methode - Slider.handle_mousemove]]
- [[Methode - Slider.draw]]

## Definiert in Datei
- [[Datei - gol app.py]]