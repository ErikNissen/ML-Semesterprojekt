from math import sqrt
from random import randint


class Robot:
    def __init__(self, startPoint, endPoint, table):
        self.x = startPoint[0]
        self.y = startPoint[1]
        self.visited = []
        self.steps = 0
        self.endPoint = endPoint
        self.table = table
        self.oldPos = None
        self.oldPositions = []

    def checkHindernis(self, direction):
        row, col = self.getPos()
        if direction == "up":
            col -= 1
        elif direction == "down":
            col += 1
        elif direction == "left":
            row -= 1
        elif direction == "right":
            row += 1
        try:
            item = self.table.item(row, col)
            cellColor = item.background().color().name()
            cellText = item.text()
        except AttributeError:
            return False
        return cellColor == "#ffff00" or cellText == "X"

    def move(self, direction):
        self.oldPos = self.getPos()
        if direction == "up":
            self.y -= 1
        elif direction == "down":
            self.y += 1
        elif direction == "left":
            self.x -= 1
        elif direction == "right":
            self.x += 1
        # If length of oldPositons is 3, overwrite first element
        if len(self.oldPositions) == 3:
            self.oldPositions[0] = self.oldPositions[1]
            self.oldPositions[1] = self.oldPositions[2]
            self.oldPositions[2] = self.getPos()
        else:
            self.visited.append(self.getPos())
            self.oldPositions.append(self.getPos())

    def getPos(self):
        return self.x, self.y

    def getoldPos(self):
        return self.oldPos

    def distance(self, point):
        return sqrt((self.x - point[0]) ** 2 + (self.y - point[1]) ** 2)

    def isStuck(self):
        # Check if Robot is stuck based on old positions
        if self.oldPositions[0] == self.oldPositions[2]:
            return True
        else:
            return False

    def movebyPoints(self):
        if self.oldPos is None:
            self.oldPos = self.getPos()
        neighbours = []
        # Sammle die Informatioen der Nachbarzellen.
        if self.x > 0:
            # rechts
            neighbours.append((self.x - 1, self.y))
        if self.x < self.table.rowCount() - 1:
            # links
            neighbours.append((self.x + 1, self.y))
        if self.y > 0:
            # hoch
            neighbours.append((self.x, self.y - 1))
        if self.y < self.table.columnCount() - 1:
            # runter
            neighbours.append((self.x, self.y + 1))

        print(f"Neighbours: {neighbours}")
        # get points of neighbours
        points = []
        # Füge alle Punkte der Nachbarn in eine Liste ein
        for n in neighbours:
            try:
                pointvalue = self.table.item(n[0], n[1]).text()
                if pointvalue == "E":
                    # Falls die Zelle der Endpunkt ist, setze die Punktzahl
                    # auf 1.
                    pointvalue = 1
                elif pointvalue == "S":
                    # Wenn die Zelle der Startpunkt ist, setze die Punktzahl
                    # auf 0.
                    pointvalue = 0
                pointvalue = float(pointvalue)
            except:
                pointvalue = 0
            print(f"Point: {pointvalue}")
            points.append(pointvalue)

        # Finde die höchste Punktzahl
        maxPoint = max(points)
        # Wähle die Zelle aus, welche die höchste Punktzahl hat.
        cell = neighbours[points.index(maxPoint)]

        # Bewege den Roboter zur ausgewählten Zelle hin.
        if cell[0] > self.x and not self.checkHindernis("right"):
            self.move("right")
        elif cell[0] < self.x and not self.checkHindernis("left"):
            self.move("left")
        elif cell[1] > self.y and not self.checkHindernis("down"):
            self.move("down")
        elif cell[1] < self.y and not self.checkHindernis("up"):
            self.move("up")
        if len(self.oldPositions) >= 3 and self.isStuck():
            # Wenn der Roboter innerhalb von drei Schritten nicht
            # weiterkommt, informiere den Nutzer
            raise Exception("Stuck")

    def randomMove(self):
        moved = False
        # Prüfe ob End Punkt sich in 1 Feld entfernung befindet
        distancetoendPoint = self.distance(self.endPoint)
        # Wird solange augeführt bis Robot ein Schritt gemacht hat
        while not moved:
            # Wird ausgeführt, wenn end Punkt sich 1 Feld entfernt befindet
            if distancetoendPoint == 1:
                # rechts
                if self.x < self.endPoint[0]:
                    self.move("right")
                # links
                elif self.x > self.endPoint[0]:
                    self.move("left")
                # runter
                elif self.y < self.endPoint[1]:
                    self.move("down")
                # hoch
                elif self.y > self.endPoint[1]:
                    self.move("up")
                moved = True
            # Geht einen random Schritt
            else:
                # Generieren random Zahl für Richtung
                direction = randint(0, 3)

                # Wenn die Zelle, zu der der Roboter gehen soll,
                # kein Hindernis ist, bewegt sich der Roboter dorthin.

                # hoch
                if direction == 0 and self.y > 0 and not self.checkHindernis(
                        "up"):
                    moved = True
                    self.move("up")
                # runter
                elif direction == 1 and self.y < 15 and not \
                        self.checkHindernis(
                                "down"):
                    moved = True
                    self.move("down")
                # links
                elif direction == 2 and self.x > 0 and not self.checkHindernis(
                        "left"):
                    moved = True
                    self.move("left")
                # rechts
                elif direction == 3 and self.x < 15 and not self.checkHindernis(
                        "right"):
                    moved = True
                    self.move("right")
