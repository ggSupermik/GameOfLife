# [[GameOfLifeModel]]

## Parametererklaerung
- [[Parameter - GameOfLifeModel.__init__.cols.md]]
- [[Parameter - GameOfLifeModel.__init__.rows.md]]

## Globale Variablen der Klasse
- `cols`: Anzahl Spalten.
- `rows`: Anzahl Reihen.
- `grid`: Bool-Grid mit Zellzustaenden.
- `generation`: Anzahl berechneter Generationen.

## Methoden
- [[Methode - GameOfLifeModel.__init__.md]]: Initialisiert leeres Grid.
- [[Methode - GameOfLifeModel.resize.md]]: Passt Gridgroesse an und erhaelt Ueberlappung.
- [[Methode - GameOfLifeModel.toggle_cell.md]]: Schaltet eine Zelle um.
- [[Methode - GameOfLifeModel.population_count.md]]: Zaehlt lebende Zellen.
- [[Methode - GameOfLifeModel.step.md]]: Berechnet naechste Generation simultan.
- [[Methode - GameOfLifeModel._count_neighbors.md]]: Zaehlt Nachbarn mit Wrap an Kanten.

## Definiert in Datei
- [[Datei - gol model.py.md]]
