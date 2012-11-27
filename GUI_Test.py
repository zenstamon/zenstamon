# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        scene = QtGui.QGraphicsScene(self)
        scene.setSceneRect(-2.0, -2.0, 4.0, 4.0)

        #fish = Fish()
        #fish.setPos(0, 0)
        scene.addItem(QtGui.QGraphicsRectItem(0, 0, 100, 100))

        view = QtGui.QGraphicsView(scene)
        view.setRenderHint(QtGui.QPainter.Antialiasing)
        view.scale(150, 150)
        self.setCentralWidget(view)


def main(args):
    app = QtGui.QApplication(args)

    win1 = MainWindow()
    win1.move(0, 0)
    win1.resize(300, 300)
    win1.show()
    win1.raise_()

    win2 = MainWindow()
    win2.move(300, 0)
    win2.resize(300, 300)
    win2.show()
    win2.raise_()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)

