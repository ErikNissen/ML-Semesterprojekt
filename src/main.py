# File: main.py

import sys
from PyQt5.QtWidgets import QApplication
from src.Graphical import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    refreshrate = app.primaryScreen().refreshRate()
    window = MainWindow(title='tbl', width=900, height=800)
    window.show()
    sys.exit(app.exec_())

"""
def draw
    mal das Feld
    
def rdmStartEnd
    random start und end punkt

def runAi
    beweg dich irgendwie durchs feld sofern noch keine Daten vorhanden
    (wenn daten vorhanden 10% chance trozdem auf ein anderes Feld zu gehen)?
    Steps[]
    run end -> rufe points auf

def pointVergabe
    Liste umdrehen
    Steps[] -> backSteps[]
    Formel: points = 0,9^backSteps[x]
    points in Feld schreiben
    x++

"""
