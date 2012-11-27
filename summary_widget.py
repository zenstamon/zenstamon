__author__ = 'c0stos3'
from PyQt4.QtCore import (Qt, SIGNAL, SLOT)
from PyQt4.QtGui import *
import sys
import os

class summary_widget(QWidget):
    def __init__(self, severity, isSmall, parent=None):
        super(summary_widget, self).__init__(parent)
        if getattr(sys, 'frozen', None):
            self.basedir = sys._MEIPASS + "\\resources\\"
        else:
            self.basedir = os.path.dirname("resources/")

        critical = severity[0]
        error = severity[1]
        warning = severity[2]

        self.sumCrit = QLabel()
        self.sumCrit.setText(" CRITICALS: " + str(critical))
        self.sumErr = QLabel("ERRORS: " + str(error))
        self.sumWarn = QLabel("WARNINGS: " + str(warning))
        self.green = QLabel("OK \t")
        self.sumCrit.setFixedSize(80, 20)
        self.sumErr.setFixedSize(70, 20)
        self.sumWarn.setFixedSize(90, 20)
        self.green.setFixedSize(50, 20
        )
        #self.sumCrit.setStyleSheet("font-size:14px;")

        summary = []
        summary.append(self.sumCrit)
        summary.append(self.sumErr)
        summary.append(self.sumWarn)

        for x in range(3):
            summary[x].setAutoFillBackground(True)
            if x == 0:
                color = "red"
                Fontcolor = "color:white"
            elif x == 1:
                color = "orange"
                Fontcolor = "color:black"
            elif x == 2:
                color = "yellow"
                Fontcolor = "color:black"

            summary[x].setStyleSheet(" background-color: " + color + "; border:1px solid #000;" + Fontcolor)
        self.green.setStyleSheet(" background-color: green; border:1px solid #000; color:white")
        self.green.hide()
        self.iconButton = QLabel()
        self.iconButton.setPixmap(QPixmap.fromImage(QImage(self.basedir + "/zenstamon_small.png")))
        self.iconButton.setAutoFillBackground(True)
        self.iconButton.setStyleSheet("color: green;font-size:14px;")
        self.iconButton.setAttribute(Qt.WA_TranslucentBackground)
        Summarylayout = QHBoxLayout()
        if isSmall == True:
            Summarylayout.addWidget(self.iconButton)
        Summarylayout.addWidget(summary[0])
        Summarylayout.addWidget(summary[1])
        Summarylayout.addWidget(summary[2])
        Summarylayout.addWidget(self.green)
        #Summarylayout.addWidget(summary[3])
        Summarylayout.insertStretch(5)
        Summarylayout.setSpacing(0)
        Summarylayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(Summarylayout)

    def updateCount(self, severity):
        self.sumCrit.setText(" CRITICALS: " + str(severity[0]))
        self.sumCrit.repaint()
        self.sumErr.setText("ERRORS: " + str(severity[1]))
        self.sumErr.repaint()
        self.sumWarn.setText("WARNINGS: " + str(severity[2]))

        if severity[0] == 0:
            self.sumCrit.hide()
        else:
            self.sumCrit.show()
        if severity[1] == 0:
            self.sumErr.hide()
        else:
            self.sumErr.show()
        if severity[2] == 0:
            self.sumWarn.hide()
        else:
            self.sumWarn.show()

        if severity[0] == 0 and severity[1] == 0 and severity[2] == 0:
            self.green.show()
        else:
            self.green.hide()
        self.sumWarn.repaint()