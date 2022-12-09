class Robot:
    def __init__(self, startPoint, endPoint, table):
        self.x = startPoint[0]
        self.y = startPoint[1]
        self.visited = []
        self.steps = 0
        self.endPoint = endPoint
        self.table = table
        self.oldPos = None

    def getMode(self):
        return self.mode

    def move(self, direction):
        if direction == "up":
            self.y -= 1
        elif direction == "down":
            self.y += 1
        elif direction == "left":
            self.x -= 1
        elif direction == "right":
            self.x += 1

    def setMode(self, mode: Mode):
        self.mode = mode

    def getPos(self):
        return self.x, self.y

    def distance(self, point):
        return sqrt((self.x - point[0]) ** 2 + (self.y - point[1]) ** 2)

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
        print(f"Neighbours: {neighbours}")
        # get points of neighbours
        points = []
        for n in neighbours:
            try:
                pointvalue = self.table.item(n[0], n[1]).text()
                if pointvalue == "E":
                    pointvalue = 1
                pointvalue = float(pointvalue)
            except:
                pointvalue = -1
            # convert #.##e+00 to float
            print(f"Point: {pointvalue}")
            points.append(pointvalue)
        # get max point
        maxPoint = max(points)
        print(f"Max Point: {maxPoint}")
        # get cell of max point
        cell = neighbours[points.index(maxPoint)]
        print(f"Cell: {cell}")
        # check where to move
        if cell[0] > self.x:
            self.move("right")
        elif cell[0] < self.x:
            self.move("left")
        elif cell[1] > self.y:
            self.move("down")
        elif cell[1] < self.y:
            self.move("up")
        if self.oldPos == self.getPos():
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