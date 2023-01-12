from random import randint
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPalette, QTextCharFormat
from PyQt5.QtWidgets import (QAbstractItemView, QHBoxLayout,
                             QLineEdit, QMainWindow, QPushButton,
                             QRadioButton,
                             QTableWidget,
                             QTableWidgetItem,
                             QTextEdit, QToolBar, QVBoxLayout, QWidget)

from src.modes import Mode
from src.Robot import Robot


class MainWindow(QMainWindow):
    def __init__(self, title, width, height, left=0, top=0):
        super().__init__()
        self.logViewer = QTextEdit()
        self.btns = []
        self.painted = []
        self.robotPosition = None
        self.hindernisse = []
        self.robot = None
        self.iterations = 1
        self.tbl = QTableWidget()
        self.title = title
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.tableColumn = 16  # create Feld
        self.tableRow = 16  # create Feld
        self.endPoint = (0, 0)
        self.startPoint = (0, 0)
        self.mode = Mode.EXPLORE
        self.boolFindWay = False

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table(row=self.tableRow, column=self.tableColumn)  # create Feld
        self.tbl.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.tbl.selectionModel().selectionChanged.connect(self.onCellClicked)
        self.tbl.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tbl.customContextMenuRequested.connect(self.onCellRightClicked)

        self.randomStartPoint()  # create startPoint
        self.randomEndPoint()  # create endPoint

        self.initRobot()

        # Create a tool bar and add the buttons as actions
        self.toolbar = QToolBar(self)
        self.logtoolbar = QToolBar(self)

        self.initToolbar()

        # Add the table widget to the central widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tbl)

        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)
        self.resize(self.tbl.width() +
                    self.toolbar.width() +
                    self.logtoolbar.width() +
                    800,
                    max(self.tbl.height(), self.toolbar.height(),
                        self.logtoolbar.height()))
        self.show()

    def initRobot(self):
        self.robot = Robot(self.startPoint, self.endPoint,
                           self.tbl)  # create Robot
        self.robotPosition = self.robot.getPos()

    def initToolbar(self):
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        # Define constants for button positions
        BTN_X_POS = 0

        # Define a list of tuples for the buttons
        buttons = [
                ("Start", self.restart, (BTN_X_POS, 0)),
                ("Automatic", self.automatic, (BTN_X_POS, 100)),
                ("Random Start/End Punkt", self.rdmStartEnd, (BTN_X_POS,
                                                              200)),
                ("Exit", self.close, (BTN_X_POS, 200))]

        # Add buttons to toolbar
        for label, callback, pos in buttons:
            self.toolbar.addWidget(self.createButton(label, callback, pos))

        # Create a widget to hold the radio buttons and input field
        widget = QWidget()

        # Use a horizontal layout to position the radio buttons and input field
        layout = QHBoxLayout()
        layout.addWidget(
                self.createInputField("Iteration", (0, 300),
                                      self.setIterations))
        exploreButton = self.createRadioButton("Explorer",
                                               self.explorerMode, (0, 0))
        exploreButton.setChecked(True)
        layout.addWidget(exploreButton)
        layout.addWidget(self.createRadioButton("Find Way",
                                                self.findWayMode, (0, 1)))

        resizeTableLayout = QHBoxLayout()

        def setRows(value):
            try:
                self.tableRow = int(value)
            except ValueError:
                self.log("Error: ", Qt.red)
                self.log(f"'{value}' als Zeilenanzahl ist ungültig.\n")

        resizeTableLayout.addWidget(
                self.createInputField(
                        "Rows", (0, 300), setRows
                )
        )

        def setCols(value):
            try:
                self.tableColumn = int(value)
            except ValueError:
                self.log("Error: ", Qt.red)
                self.log(f"'{value}' als Spaltenanzahl ist ungültig.\n")

        resizeTableLayout.addWidget(
                self.createInputField(
                        "Columns", (0, 300), setCols
                )
        )

        # Erstelle Tablle mit benutzerdefinierten Spalten und Zeilen
        def resizeTable():
            self.tbl.setRowCount(self.tableRow)
            self.tbl.setColumnCount(self.tableColumn)
            self.tbl.setHorizontalHeaderLabels([str(i) for i in range(
                    self.tableColumn)])
            self.tbl.setVerticalHeaderLabels(
                    [str(i) for i in range(self.tableRow)])
            self.tbl.resizeColumnsToContents()
            self.tbl.resizeRowsToContents()
            self.tbl.move(0, 0)
            self.tbl.repaint()
            self.rdmStartEnd()

        resizeTableLayout.addWidget(
                self.createButton(
                        "Resize", resizeTable, (0, 300)
                )
        )

        resizeTableWidget = QWidget()
        resizeTableWidget.setLayout(resizeTableLayout)

        widget.setLayout(layout)

        # Add the widget to the tool bar
        self.toolbar.addWidget(widget)
        self.toolbar.addWidget(resizeTableWidget)

        # Set the orientation of the toolbar to be vertical
        self.toolbar.setOrientation(Qt.Vertical)

        self.initLog()
        self.addToolBar(Qt.RightToolBarArea, self.logtoolbar)

    def initLog(self):
        self.logViewer.setFixedHeight(self.size().height())
        themeButton = QPushButton("Switch Background Color")

        def toggleBackgroundColor():
            palette = self.logViewer.palette()
            _, _, v, _ = palette.color(QPalette.Base).getHsv()
            if v > 0.5:
                palette.setColor(QPalette.Base, Qt.black)
            else:
                palette.setColor(QPalette.Base, Qt.white)
            self.logViewer.setPalette(palette)

        themeButton.clicked.connect(toggleBackgroundColor)

        self.logtoolbar.addWidget(self.logViewer)
        self.logtoolbar.addWidget(themeButton)

    def log(self, info, color=Qt.white, bold=False):
        print(info, end="")
        charFormat = QTextCharFormat()
        charFormat.setFontPointSize(10)
        charFormat.setForeground(color)
        if bold:
            charFormat.setFontWeight(QFont.Bold)
        cur = self.logViewer.textCursor()
        cur.insertText(info, charFormat)
        cur.movePosition(cur.End)
        self.logViewer.ensureCursorVisible()
        self.logViewer.adjustSize()
        self.logViewer.update()
        self.logtoolbar.adjustSize()
        self.logtoolbar.update()
        self.resize(self.tbl.columnCount() * 50 +
                    self.toolbar.width() +
                    self.logtoolbar.width(),
                    max(self.tbl.height(), self.toolbar.height(),
                        self.logtoolbar.height()))
        self.update(end=True)

    # mit MB1 kann Hinderniss erstellt werden
    def onCellClicked(self, selected, _):
        sr, sc = self.startPoint
        er, ec = self.endPoint
        for cell in selected.indexes():
            if cell == self.startPoint or cell == self.endPoint:
                continue
            if self.istPathClear(sr, sc, er, ec):
                row, col = cell.row(), cell.column()
                self.painted.append((row, col))
                self.tbl.setItem(row, col, QTableWidgetItem("X"))
                self.tbl.item(row, col).setBackground(QColor("#ffff00"))
                self.tbl.item(row, col).setSelected(False)
                self.tbl.repaint()
            else:
                self.log("Error: ", Qt.red)
                self.log("Roboter kann nicht das Ziel erreichen!\n")
        while not self.istPathClear(sr, sc, er, ec):
            row, col = self.painted.pop()
            self.tbl.item(row, col).setBackground(Qt.transparent)
            self.tbl.item(row, col).setText("")
            self.tbl.item(row, col).setSelected(False)
            self.tbl.repaint()

    # mit MB2 kann Hinderniss entfernt werden
    def onCellRightClicked(self, pos):
        index = self.tbl.indexAt(pos)
        if index.isValid():
            row, col = index.row(), index.column()
            if (row, col) in self.painted:
                self.tbl.item(row, col).setText("")
                self.tbl.item(row, col).setBackground(Qt.transparent)
                self.painted.remove((row, col))
                self.tbl.repaint()

    # Prüft, ob man vom Start Punkt immer noch zum Endpunkt kommen kann wenn
    # nicht wird eine Hinderniss Zelle entfernt
    def istPathClear(self, startRow, startCol, endRow, endCol):
        # Set, um besuchte Positionen zu speichern
        visited = set()

        def dfs(row, col):
            # Basisfall: Wenn die aktuelle Position die Zielposition ist, gib true zurück
            if (row, col) == (endRow, endCol):
                return True

            try:
                # Wenn die aktuelle Position bereits besucht wurde oder eine
                # Hintergrundfarbe von gelb hat, gib false zurück
                if (row, col) in visited or self.tbl.item(row, col).background().color().name() == "#ffff00":
                    return False
            except AttributeError:
                pass

            # Markiere die aktuelle Position als besucht
            visited.add((row, col))

            # Rufe die Funktion rekursiv für die Positionen über, unter, links und rechts der aktuellen Position auf
            if row > 0:
                if dfs(row - 1, col):
                    return True
            if row < self.tbl.rowCount() - 1:
                if dfs(row + 1, col):
                    return True
            if col > 0:
                if dfs(row, col - 1):
                    return True
            if col < self.tbl.columnCount() - 1:
                if dfs(row, col + 1):
                    return True

            # Wenn kein Aufruf true zurückgibt, gib false zurück
            return False

        # Initialer Aufruf, um die DFS-Algorithmus zu starten
        return dfs(startRow, startCol)



    def automatic(self):
        self.mode = Mode.EXPLORE
        self.restart(0)
        self.mode = Mode.BYPOINTS
        self.restart(0)

    def explorerMode(self):
        print("Explorer Mode")
        self.mode = Mode.EXPLORE

    def findWayMode(self):
        print("Find Way Mode")
        self.mode = Mode.BYPOINTS

    def table(self, row, column):  # create Feld
        self.tbl.setRowCount(row)
        self.tbl.setColumnCount(column)
        self.tbl.horizontalHeader().setStyleSheet("QHeaderView::section { "
                                                  "background-color: "
                                                  "orange; color: blue;}")
        self.tbl.setHorizontalHeaderLabels([str(i) for i in range(column)])
        self.tbl.verticalHeader().setStyleSheet("QHeaderView::section { "
                                                "background-color: cyan; "
                                                "color: #8B0000}")
        self.tbl.setVerticalHeaderLabels([str(i) for i in range(row)])
        self.tbl.resizeColumnsToContents()
        self.tbl.resizeRowsToContents()
        self.tbl.move(0, 0)
        self.tbl.show()

    def rdmStartEnd(self):
        self.clearTable()
        self.boolFindWay = False
        self.update(end=True)
        self.randomStartPoint()
        self.randomEndPoint()

    def randomStartPoint(self):
        while True:
            try:
                row, column = randint(0, self.tbl.rowCount()), randint(0, self.tbl.columnCount())
                self.tbl.setItem(row, column, QTableWidgetItem("Start"))
                self.tbl.item(row, column).setBackground(QColor(0, 255, 0))
                self.startPoint = (row, column)
                break
            except:
                pass
    def randomEndPoint(self):
        while True:
            row, column = randint(0, self.tbl.rowCount()), randint(0, self.tbl.columnCount())
            if self.tbl.item(row, column) != QTableWidgetItem("Start"):
                try:
                    self.tbl.setItem(row, column, QTableWidgetItem("End"))
                    self.tbl.item(row, column).setBackground(QColor(255, 0, 0))
                    break
                except AttributeError:
                    pass
        self.endPoint = (row, column)


    def paintCell(self, row, column, color, name="", oldcolor=None, alpha=1):
        if oldcolor is not None:
            color.setAlpha(oldcolor.alpha() + 1)
        else:
            color.setAlpha(alpha)
        self.tbl.setItem(row, column, QTableWidgetItem(name))
        self.tbl.item(row, column).setBackground(color)

    def setPoints(self, value, cell):
        # format value to #.##e+00
        value = f"{value:.2e}"
        # schreibe value in Zelle
        self.tbl.item(cell[0], cell[1]).setText(value)
        # reset Hintergrundsfarbe
        self.tbl.item(cell[0], cell[1]).setBackground(QColor('transparent'))
        self.tbl.item(self.endPoint[0], self.endPoint[1]).setBackground(
                QColor(255, 0, 0))
        self.tbl.item(self.startPoint[0], self.startPoint[1]).setBackground(
                QColor(0, 255, 0))
        # ändert bei zu großen Zahlen die Schriftgröße in den Zellen
        self.tbl.resizeColumnsToContents()
        self.tbl.resizeRowsToContents()

    """
        Die Methode run ist die Hauptschleife des Programms und steuert den Bewegungsablauf des Robots. 
        Sie verwendet eine while-Schleife, die solange läuft, bis der Roboter seinen Endpunkt erreicht hat.
    """
    def run(self, delay=1 / 144):
        cancel = False
        try:
            # Der Roboter wird solange bewegt, bis er sein Ziel erreicht hat.
            while self.robotPosition != self.endPoint:
                # Überprüfung ob der Modus "EXPLORE" oder "BYPOINTS" aktiviert ist.
                if self.mode == Mode.EXPLORE:
                    # Wenn "EXPLORE" aktiviert ist, wird der Roboter
                    # zufällig bewegt und der bool "FindWay" auf true gesetzt.
                    self.robot.randomMove()
                    self.boolFindWay = True
                elif self.mode == Mode.BYPOINTS:
                    # Wenn "BYPOINTS" aktiviert ist und boolFindWay true ist,
                    # bewegt sich der Roboter aufgrund der erhaltenen Punkte,
                    # ansonsten wird eine Fehlermeldung ausgegeben und die Schleife beendet.
                    if self.boolFindWay:
                        try:
                            self.robot.movebyPoints()
                        except:
                            cancel = True
                            break
                    else:
                        print("Need to Explorer First!")
                        break
                # Aktualisiere die Position des Roboters.
                self.robotPosition = self.robot.getPos()
                if self.robotPosition not in self.robot.visited:
                    # Falls die Position des Roboters noch nicht in visited
                    # ist, füge diese hinzu.
                    self.robot.visited.append(self.robotPosition)

                self.robot.steps += 1
                # Aktualisiere die GUI
                self.update()
                # Wartet eine kurze Zeit (in ms) bevor ein weiteren Schritt macht.
                sleep(delay)

                # logging
                self.log("Robot Position:", Qt.cyan, bold=True)
                self.log(f" R{self.robotPosition[0]} ", QColor("#ffa500"))
                self.log(f"C{self.robotPosition[1]}\n", Qt.cyan)

            if cancel:
                # Falls der Roboter in einer Endlosschleife ist, informiere
                # den Nutzer.
                self.log(f"Robot stops at position {self.robot.getPos()}\n",
                         Qt.red)

            # logging
            self.log("Robot Steps:", Qt.green, bold=True)
            self.log(f"{self.robot.steps}\n")

            # Invertiere die visited liste für die Punktevergabe.
            backvisited = self.robot.visited[::-1]
            # b = Schritt zähler
            for b in range(len(backvisited)):
                # back = position zu dem entsprechnden schritt
                back = backvisited[b]
                if back == self.endPoint or back == self.startPoint:
                    # Wenn die aktuelle Position der Start/Endpunkt ist,
                    # überspringe diese.
                    continue

                # Kalkuliere die Punktzahl des aktuellen Feldes.
                points = 0.9 ** b
                cellPoints = None
                try:
                    if self.mode == Mode.BYPOINTS:
                        # Falls der Modus "BYPOINTS" ist und das aktuelle
                        # Feld eine Punktzahl hat, speichere diese in
                        # cellPoints.
                        cellPoints = float(self.tbl.item(back[1], back[0]).text())
                except:
                    cellPoints = None

                # Berechnen des neuen Punktwerts für die Zelle
                if cellPoints is not None:
                    median = (points + cellPoints) / 2
                    points += median
                elif cellPoints == 0:
                    points = 0

                # # logging
                self.log(f"{b}:", Qt.yellow)
                self.log(f" {points:.2e} ", Qt.magenta, bold=True)
                row, col = self.robot.visited[b]
                self.log("Punkte bei Position: ")
                self.log(f"R{row} ", QColor("#ffa500"))
                self.log(f"C{col}\n", Qt.cyan)

                # Setzen des Punktwerts in der Tabelle
                self.setPoints(points, back)
        except Exception as e:
            print(e)

    def clearTable(self):
        for row in range(self.tbl.rowCount()):
            for column in range(self.tbl.columnCount()):
                try:
                    self.tbl.item(row, column).setText("")
                except:
                    pass
                try:
                    self.tbl.item(row, column).setBackground(
                            QColor('transparent'))
                except:
                    pass


    def restart(self, delay=1 / 144):
        for _ in range(0, self.iterations):
            for x in range(self.tableRow):
                for y in range(self.tableColumn):
                    try:
                        if self.tbl.item(x, y).background().color().name() \
                                == "#ffff00":
                            continue
                        self.tbl.item(x, y).setBackground(QColor(
                                'transparent'))
                    except AttributeError:
                        pass
            self.robot = Robot(self.startPoint, self.endPoint, self.tbl)
            self.robotPosition = self.robot.getPos()
            self.update()
            self.run(delay)


    def createButton(self, name, function, position):
        button = QPushButton(name, self)
        button.move(position[0], position[1])
        button.clicked.connect(function)
        return button


    def createRadioButton(self, name, function, position):
        radio = QRadioButton(name, self)
        radio.move(position[0], position[1])
        radio.clicked.connect(function)
        return radio


    def createInputField(self, name, position, function):
        inputbox = QLineEdit(self)
        inputbox.move(position[0], position[1])
        inputbox.setPlaceholderText(name)
        inputbox.textChanged.connect(function)
        return inputbox


    def setIterations(self, value: str):
        if value == "":
            value = 1
        elif not value.isdigit():
            self.log(f"Error: {value} ist keine Zahl.\n", Qt.red)
        elif int(value) <= 0:
            value = 1
        else:
            print("Changed to: " + value)
            self.iterations = int(value)


    def update(self, end=False) -> None:
        super().update()
        self.repaint()
        if not end:
            for i in self.robot.visited:
                if self.mode == Mode.BYPOINTS:
                    continue
                # get color of cell
                try:
                    oldcolor = self.tbl.item(i[0], i[1]).background().color()
                except AttributeError:
                    oldcolor = None
                self.paintCell(i[0], i[1], QColor(0, 0, 255, 1), "", oldcolor,
                               1)
            alpha = self.tbl.item(self.robotPosition[0], self.robotPosition[
                1]).background().color().alpha()
            if self.mode == Mode.BYPOINTS:
                self.paintCell(self.robotPosition[0], self.robotPosition[1],
                               QColor(255,215,0),
                               alpha=255)
            else:
                self.paintCell(self.robotPosition[0], self.robotPosition[1],
                               QColor(255, 255, 0), "R", alpha=alpha)
            self.paintCell(self.startPoint[0], self.startPoint[1],
                           QColor(0, 255, 0), "S", alpha=255)
            self.paintCell(self.endPoint[0], self.endPoint[1],
                           QColor(255, 0, 0), "E", alpha=255)
