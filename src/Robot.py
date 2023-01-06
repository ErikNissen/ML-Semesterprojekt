from collections import deque
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
        self.oldPositions = deque(maxlen=3)

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
        if len(self.oldPositons) == 3:
            self.oldPositons[0] = self.oldPositons[1]
            self.oldPositons[1] = self.oldPositons[2]
            self.oldPositons[2] = self.getPos()
        else:
            self.oldPositons.append(self.getPos())

    def getPos(self):
        return self.x, self.y

    def getoldPos(self):
        return self.oldPos

    def distance(self, point):
        return sqrt((self.x - point[0]) ** 2 + (self.y - point[1]) ** 2)

    def checkhinderniss(self, direction):
        # Get Background Color of Cell
        try:
            if direction == "up":
                color = self.table.item(self.x, self.y - 1).background()
            elif direction == "down":
                color = self.table.item(self.x, self.y + 1).background()
            elif direction == "left":
                color = self.table.item(self.x - 1, self.y).background()
            elif direction == "right":
                color = self.table.item(self.x + 1, self.y).background()
        except:
            return False
        # Check if Color is White
        if color == "#ffffff":
            return True
        else:
            return False

    def isStuck(self):
        # Check if Robot is stuck based on old positions
        if self.oldPositons[0] == self.oldPositons[2]:
            return True
        else:
            return False

    def movebyPoints(self):
        if self.oldPos is None:
            self.oldPos = self.getPos()
        neighbours = []
        if self.x > 0:
            # right
            neighbours.append((self.x - 1, self.y))
        if self.x < self.table.rowCount() - 1:
            # left
            neighbours.append((self.x + 1, self.y))
        if self.y > 0:
            # up
            neighbours.append((self.x, self.y - 1))
        if self.y < self.table.columnCount() - 1:
            # down
            neighbours.append((self.x, self.y + 1))
        # Remove all cells with background color white
        for neighbour in neighbours:
            try:
                if self.table.item(neighbour[0],
                                   neighbour[1]).background() == "#ffffff":
                    neighbours.remove(neighbour)
            except AttributeError:
                pass
        print(f"Neighbours: {neighbours}")
        # get points of neighbours
        points = []
        for n in neighbours:
            try:
                pointvalue = self.table.item(n[0], n[1]).text()
                if pointvalue == "E":
                    pointvalue = 1
                elif pointvalue == "S":
                    pointvalue = -1
                pointvalue = float(pointvalue)
            except:
                pointvalue = 0
            # convert #.##e+00 to float
            print(f"Point: {pointvalue}")
            points.append(pointvalue)
        # get max point
        maxPoint = max(points)
        # get cell of max point
        cell = neighbours[points.index(maxPoint)]
        # check where to move
        if cell[0] > self.x and not self.checkhinderniss("right"):
            self.move("right")
        elif cell[0] < self.x and not self.checkhinderniss("left"):
            self.move("left")
        elif cell[1] > self.y and not self.checkhinderniss("down"):
            self.move("down")
        elif cell[1] < self.y and not self.checkhinderniss("up"):
            self.move("up")
        if len(self.oldPositons) >= 3 and self.isStuck():
            print("Stuck")
            raise Exception("Stuck")

    def randomMove(self):
        moved = False
        distancetoendPoint = self.distance(self.endPoint)
        while not moved:
            if distancetoendPoint == 1:
                if self.x < self.endPoint[0]:
                    self.move("right")
                elif self.x > self.endPoint[0]:
                    self.move("left")
                elif self.y < self.endPoint[1]:
                    self.move("down")
                elif self.y > self.endPoint[1]:
                    self.move("up")
                moved = True
            else:
                direction = randint(0, 3)
                if direction == 0 and self.y > 0:
                    moved = True
                    self.move("up")
                elif direction == 1 and self.y < 15:
                    moved = True
                    self.move("down")
                elif direction == 2 and self.x > 0:
                    moved = True
                    self.move("left")
                elif direction == 3 and self.x < 15:
                    moved = True
                    self.move("right")
