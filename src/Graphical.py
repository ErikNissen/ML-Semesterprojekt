import asyncio
import sys
import threading
from random import randint
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QTextCharFormat, QTextOption
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout,
                             QHeaderView,
                             QLineEdit, QMainWindow, QPushButton,
                             QRadioButton,
                             QTableWidget,
                             QTableWidgetItem,
                             QTextEdit, QToolBar, QVBoxLayout, QWidget)

from src.Log import LogWindow
from src.modes import Mode
from src.Robot import Robot
from colorama import Fore, Style


class MainWindow(QMainWindow):
    def __init__(self, title, width, height, left=0, top=0):
        super().__init__()
        self.logViewer = QTextEdit()
        self.btns = []
        self.robotPosition = None
        self.hindernisswidth = None
        self.hindernissheight = None
        self.hindernissY = None
        self.hindernissX = None
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
        layout.addWidget(self.createRadioButton("Explorer",
                                                self.explorerMode, (0, 0)))
        layout.addWidget(self.createRadioButton("Find Way",
                                                self.findWayMode, (0, 1)))

        widget.setLayout(layout)

        # Add the widget to the tool bar
        self.toolbar.addWidget(widget)

        # Set the orientation of the toolbar to be vertical
        self.toolbar.setOrientation(Qt.Vertical)

        self.initLog()
        self.addToolBar(Qt.RightToolBarArea, self.logtoolbar)

    def initLog(self):
        self.logViewer.setFixedHeight(self.size().height())
        self.logtoolbar.addWidget(self.logViewer)

    def log(self, info, color=Qt.white, bold=False):
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
        self.resize(self.tbl.columnCount()*50 +
                    self.toolbar.width() +
                    self.logtoolbar.width(),
                    max(self.tbl.height(), self.toolbar.height(),
                        self.logtoolbar.height()))
        self.update()

    def buttons(self):
        self.btns.append(self.createButton("Start", self.restart, (0, 0)))
        self.btns.append(self.createButton("Automatic", self.automatic, (0,
                                                                         100)))
        self.btns.append(
                self.createButton("Random Start/End Punkt", self.rdmStartEnd,
                                  (0, 200)))
        self.btns.append(self.createButton("Exit", self.close, (0, 200)))

        radiobtnlayout = QHBoxLayout()

        explore = self.createRadioButton(
                "Explorer", self.explorerMode, (0, 200))
        explore.setChecked(True)
        iteration = self.createInputField("Iteration", (0, 300),
                                          self.setIterations)
        radiobtnlayout.addWidget(iteration)
        radiobtnlayout.addWidget(explore)
        radiobtnlayout.addWidget(self.createRadioButton(
                "Find Way", self.findWayMode, (0, 400)))  # "Find Way" kann
        # nur benutzt werden, wenn mindestens 1 Explor gemacht wurde
        self.layout.addLayout(radiobtnlayout)

    def hindernissMenu(self):
        layout = QHBoxLayout()
        layout.addWidget(
                self.createButton("Erstell Hinderniss", self.createHinderniss,
                                  (0,
                                   200)))
        xInput = self.createInputField("X", (0, 200), self.setHindernissX)
        yInput = self.createInputField("Y", (0, 200), self.setHindernissY)
        widthInput = self.createInputField("Width", (0, 200),
                                           self.setHindernisswidth)
        heightInput = self.createInputField("Height", (0, 200),
                                            self.setHindernissheight)

        layout.addWidget(xInput)
        layout.addWidget(yInput)
        layout.addWidget(widthInput)
        layout.addWidget(heightInput)
        self.layout.addLayout(layout)

    def setHindernissX(self, x):
        if int(x) < 0:
            x = 0
        elif int(x) > self.tableColumn:
            x = self.tableColumn
        else:
            self.hindernissX = int(x)

    def setHindernissY(self, y):
        if int(y) < 0:
            y = 0
        elif int(y) > self.tableRow:
            y = self.tableRow
        else:
            self.hindernissY = int(y)

    def setHindernisswidth(self, width):
        if int(width) < 0:
            radius = 0
        elif int(width) > self.tableColumn:
            radius = self.tableColumn
        self.hindernisswidth = int(width)

    def setHindernissheight(self, height):
        if int(height) < 0:
            radius = 0
        elif int(height) > self.tableRow:
            radius = self.tableRow
        self.hindernissheight = int(height)

    def checkHinterniss(self):
        # Check if the start or end point is in hinderniss
        if self.hindernissX is not None and self.hindernissY is not None and self.hindernisswidth is not None and self.hindernissheight is not None:
            # Check if start point is in hinderniss
            if self.hindernissX - self.hindernisswidth / 2 <= self.startPoint[
                0] <= self.hindernissX + self.hindernisswidth / 2 and self.hindernissY - self.hindernissheight / 2 <= \
                    self.startPoint[
                        1] <= self.hindernissY + self.hindernissheight / 2:
                # if start point is in hinderniss, return false
                return False
            # Check if end point is in hinderniss
            if self.hindernissX - self.hindernisswidth / 2 <= self.endPoint[
                0] <= self.hindernissX + self.hindernisswidth / 2 and self.hindernissY - self.hindernissheight / 2 <= \
                    self.endPoint[
                        1] <= self.hindernissY + self.hindernissheight / 2:
                # if end point is in hinderniss, return false
                return False
            # if start and end point are not in hinderniss, return true
        return True

    def createHinderniss(self):
        if self.checkHinterniss():
            for x in range(self.hindernisswidth):
                for y in range(self.hindernissheight):
                    self.tbl.setItem(self.hindernissX + x,
                                     self.hindernissY + y,
                                     QTableWidgetItem(""))
                    self.tbl.item(self.hindernissX + x,
                                  self.hindernissY + y).setBackground(QColor(
                            255, 255, 255))
        else:
            print("Start or End point is in hinderniss")

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
        self.tbl.setHorizontalHeaderLabels([str(i) for i in range(column)])
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

    def randomStartPoint(self):  # create Start Point and draw in tbl
        column = randint(0, self.tbl.columnCount())
        row = randint(0, self.tbl.rowCount())
        success = False
        while not success:
            try:
                self.startPoint = (row, column)

                self.tbl.setItem(row, column, QTableWidgetItem("Start"))
                self.tbl.item(row, column).setBackground(QColor(0, 255, 0))
                success = True
            except:
                pass

    def randomEndPoint(self):  # create End Point and draw in tbl
        success = False
        column = randint(0, self.tbl.columnCount())
        row = randint(0, self.tbl.rowCount())
        while self.tbl.item(row, column) == QTableWidgetItem("Start"):
            column = randint(0, self.tbl.columnCount())
            row = randint(0, self.tbl.rowCount())
        # check if End Point is not Start Point
        while not success:
            try:
                self.endPoint = (row, column)
                self.tbl.setItem(row, column, QTableWidgetItem("End"))
                self.tbl.item(row, column).setBackground(QColor(255, 0, 0))
                success = True
            except AttributeError:
                pass

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
        self.tbl.item(cell[0], cell[1]).setText(value)
        self.tbl.item(cell[0], cell[1]).setBackground(
                QColor(255, 255, 255, 100))
        self.tbl.item(self.endPoint[0], self.endPoint[1]).setBackground(
                QColor(255, 0, 0))
        self.tbl.item(self.startPoint[0], self.startPoint[1]).setBackground(
                QColor(0, 255, 0))
        self.tbl.resizeColumnsToContents()
        self.tbl.resizeRowsToContents()

    def run(self, delay=1 / 144):
        while self.robotPosition != self.endPoint:
            if self.mode == Mode.EXPLORE:
                self.robot.randomMove()
                self.boolFindWay = True
            elif self.mode == Mode.BYPOINTS:
                if self.boolFindWay:
                    self.robot.movebyPoints()
                else:
                    print("Need to Explorer First!")
                    break
            self.robotPosition = self.robot.getPos()
            if self.robotPosition not in self.robot.visited:
                self.robot.visited.append(self.robotPosition)
            self.robot.steps += 1
            self.log("Robot Position:", Qt.cyan, bold=True)
            self.log(f" {self.robotPosition}\n")
            self.update()
            sleep(delay)
        self.log("Robot Steps:", Qt.green, bold=True)
        self.log(f"{self.robot.steps}\n")

        backvisited = self.robot.visited[::-1]
        for b in range(len(backvisited)):
            if backvisited[b] == self.endPoint:
                continue

            points = 0.9 ** b
            cellPoints = 0
            try:
                # get CellPoints value
                cellPoints = float(
                        self.tbl.item(backvisited[b][0],
                                      backvisited[b][1]).text())
            except:
                pass
            # if cellPoints != 0
            if cellPoints != 0:
                # median = (points+"cellpoints")/2
                median = (points + cellPoints) / 2
                # points += median
                points += median

            self.log(f"{b}:", Qt.yellow)
            self.log(f" {points:.2e} ", Qt.magenta, bold=True)
            self.log("Punkte bei Position:"
                     f" {self.robot.visited[b]}\n")
            self.setPoints(points, backvisited[b])
            self.update(end=True)

    def clearTable(self):
        for row in range(self.tbl.rowCount()):
            for column in range(self.tbl.columnCount()):
                try:
                    self.tbl.item(row, column).setText("")
                except:
                    pass
                try:
                    self.tbl.item(row, column).setBackground(
                            QColor(75, 75, 75))
                except:
                    pass

    def restart(self, delay=1 / 144):
        for _ in range(0, self.iterations):
            for x in range(self.tableRow):
                for y in range(self.tableColumn):
                    try:
                        self.tbl.item(x, y).setBackground(QColor(75, 75, 75))
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

    def setIterations(self, value):
        print("Changed to: " + value)
        if value == "":
            value = 1
        self.iterations = int(value)

    def update(self, end=False) -> None:
        super().update()
        self.repaint()
        if not end:
            for i in self.robot.visited:
                # get color of cell
                try:
                    oldcolor = self.tbl.item(i[0], i[1]).background().color()
                except AttributeError:
                    oldcolor = None
                self.paintCell(i[0], i[1], QColor(0, 0, 255, 1), "", oldcolor,
                               1)
            alpha = self.tbl.item(self.robotPosition[0], self.robotPosition[
                1]).background().color().alpha()
            self.paintCell(self.robotPosition[0], self.robotPosition[1],
                           QColor(255, 255, 0), "R", alpha=alpha)
            self.paintCell(self.startPoint[0], self.startPoint[1],
                           QColor(0, 255, 0), "S", alpha=255)
            self.paintCell(self.endPoint[0], self.endPoint[1],
                           QColor(255, 0, 0), "E", alpha=255)
