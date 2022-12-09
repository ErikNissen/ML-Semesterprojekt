import sys
from PyQt5.QtWidgets import *

from src.Graphical import MainWindow

# ToDo: Solve!
# ToDo 1: run / restart darf text in Zellen nicht überschrieben!
# ToDo 3: Endpunkt gibt 1 punkte => ist von anfang an gesetz und kann nicht umgeschrieben werden(?!) => Ziel Schritt wird Priorisiert
# ToDo 5: non-/Explorer mode einbauen => "läuft den punkten hinterher" => Checkbox benötigt?
# ToDo 5 -> keine Checkbox, nutzen 2 buttons: Button 1 "Explorer" | Button 2: "Find Way"
# ToDo 4: wenn Feld Punkte hat, AI darf NICHT zurücklaufen um punkte
#  mehrfach einzustecken (?!) - AI Minuspunkte geben => wird doch nich benötigt!
# ToDo 6: button einbauen um Start-/Endpunkt zu ändern - gesetzte Punkte bleiben in den Zellen erhalten! => S & E bleiben vorhanden, wenn nicht rübergelaufen wurde

# ToDO: WIP
# ToDo 2: Punkte vergabe: wenn im Feld bereits punkte vorhanden sind nehme den Mittelwert aus beiden Zahlen
# ToDo 7: Hindernisse einbauen
#  WICHTIG!! Hindernisse müssen so gebaut sein das man noch zum Ziel kommt
#  (Optional) Sowohl random als auch feste strecken

# ToDo: Open
#  Parameterisieren:
#   Tabel Größe (X, Y) im nachhinein vergrößern oder verkleinern können -> new draw


if __name__ == '__main__':
    app = QApplication(sys.argv)
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
