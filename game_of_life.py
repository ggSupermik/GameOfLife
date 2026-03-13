from random import *
class game_of_life:

    def __init__(self, x = 50, y = 50, Runden = 5):
        #Erstellt das Spielfeld
        self.x = x
        self.y = y
        self.Runden = Runden
        self.matrix = list(range(x))

        for i in range(len(self.matrix)):
            self.matrix[i] = list(range(y))
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = randrange(0, 2)

    def starting_point(self, x, y):
        #Setzt einen Punkt an die Coordinate im Spielfeld
        self.matrix[x][y] = 1
        
        
    def spielfeld_anzeigen(self):
        
        for i in range(self.y):
            x_row = []
            for j in range(self.x):
                x_row.append(self.matrix[j][i])
            print(x_row)

    def count_fields(self, x, y):

        count = 0
        try:
                    
            if self.matrix[x-1][y-1] == 1:
                count += 1
            if self.matrix[x][y-1] == 1:
                count += 1
            if self.matrix[x+1][y-1] == 1:
                count += 1
            if self.matrix[x-1][y] == 1:
                count += 1
            if self.matrix[x+1][y] == 1:
                count += 1
            if self.matrix[x-1][y+1] == 1:
                count += 1
            if self.matrix[x][y+1] == 1:
                count += 1
            if self.matrix[x+1][y+1] == 1:
                count += 1
                        
        except:
                    
            pass
                
        return count

    def birth_point(self, x, y):

        if self.count_fields(x, y) == 3 and self.matrix[x][y] == 0:

            self.matrix[x][y] = 1

    def survive_point(self, x, y):

        if (self.count_fields(x, y) == 2 or self.count_fields(x, y) == 3) and self.matrix[x][y] == 1:

            self.matrix[x][y] = 1

    def death_point(self, x, y):

        if (self.count_fields(x, y) <= 1 or self.count_fields(x, y) >= 3) and self.matrix[x][y] == 1:

            self.matrix[x][y] = 0

    def check_rules(self, x, y):

        self.birth_point(x, y)
        self.survive_point(x, y)
        self.death_point(x, y)

    def main_loop(self):
        Runde = 0
        
        while Runde <= self.Runden:
            Runde += 1
            print('Runde: ', Runde)
            for i in range(self.x):
                for j in range(self.y):

                    self.check_rules(i, j)
    
            self.spielfeld_anzeigen()
        
test = game_of_life()
test.spielfeld_anzeigen()
'''
test.starting_point(2, 1)
test.starting_point(3, 1)
test.starting_point(3, 2)
test.starting_point(2, 2)
test.starting_point(5, 5)
test.starting_point(5, 6)
test.starting_point(4, 5)
test.starting_point(3, 4)
test.starting_point(2, 3)
'''
test.main_loop()

            
