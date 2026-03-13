# [[GameOfLifeModel]]

## Parametererklaerung
- [[Parameter - GameOfLifeModel.__init__.cols]]
- [[Parameter - GameOfLifeModel.__init__.rows]]

## Globale Variablen der Klasse
- `cols`: Anzahl Spalten.
- `rows`: Anzahl Reihen.
- `grid`: Bool-Grid mit Zellzustaenden.
- `generation`: Anzahl berechneter Generationen.

## Methoden
- [[Methode - GameOfLifeModel.__init__]]: Initialisiert leeres Grid.
- [[Methode - GameOfLifeModel.resize]]: Passt Gridgroesse an und erhaelt Ueberlappung.
- [[Methode - GameOfLifeModel.toggle_cell]]: Schaltet eine Zelle um.
- [[Methode - GameOfLifeModel.population_count]]: Zaehlt lebende Zellen.
- [[Methode - GameOfLifeModel.step]]: Berechnet naechste Generation simultan.
- [[Methode - GameOfLifeModel._count_neighbors]]: Zaehlt Nachbarn mit Wrap an Kanten.

## Definiert in Datei
- [[Datei - gol model.py]]
