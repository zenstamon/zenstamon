__author__ = 'c0stos3'



#! /usr/bin/python

# -*- coding : utf-8 -*-

from PyQt4 import QtGui, QtCore

import time, sys

gui = QtGui.QApplication.processEvents #a function we use to make sure that the gui wont freeze

class display():#first we make a class that handle the gui object

    texttoset = ""

    app = QtGui.QApplication(sys.argv) #we make a QT Application object

    dialog = QtGui.QDialog() #we make a dialog object

    dialog.resize(200, 150) #set size

    dialog.setMaximumSize(200, 150) #set maximum size

    dialog.setMinimumSize(200, 150) #set minimum size

    dialog.setWindowTitle("new dialog") #set title

    label = QtGui.QLabel(dialog) #make a label object child of dialog

    label.setText("am a text label") #set label text

    label.setGeometry(1, 20, 200, 50)#set geometry x,y,width,high

    button = QtGui.QPushButton(dialog)#now we make a button object

    button.setText("click me !")#set its text

    button.setGeometry(1, 60, 200, 50)#set geometry

    def changetext(self, value):#we make a function that change the label text

        if value == True:
            text = str(self.texttoset)#to make sure it will be a string

            self.label.setText(text)#set the text

ui = display()#we make  an object  from the display class

#now it is time to make a QThread class

class mythread(QtCore.QThread):#inherite from QtCore.QThread

    #this thread will change the text 10 times from "i have changed by a QThread" to "back all over again for the x time" then when finished changes text to "QThread has finished"

    def __init__(self):
        QtCore.QThread.__init__(self)#we construct the class

    def run(self):#built in function contain the code that the thread will excute

        x = 0

        while x <= 10:
            s = str(x)

            display.texttoset = "i have changed by a QThread"#set the text wich the changetext function will display

            self.emit(QtCore.SIGNAL("anysignalname(bool)"),
                True) #we send the signal called "anysignalname" and send a bool argument

            time.sleep(1)#sleep for 1 sec

            gui()#refresh the gui

            display.texttoset = "back all over again for " + s + " time"#set the text wich the changetext function will display

            self.emit(QtCore.SIGNAL("anysignalname(bool)"),
                True) #we send the signal called "anysignalname" and send a bool argument

            time.sleep(1)#sleep for 1 sec

            gui()#refresh the gui

            x = x + 1 #increase x value

        display.texttoset = "QThread has finished!!"#set the text wich the changetext function will display

        self.emit(QtCore.SIGNAL("anysignalname(bool)"),
            True) #we send the signal called "anysignalname" and send a bool argument

        time.sleep(1)#sleep for 1 sec

        gui()#refresh the gui


thread1 = mythread()#we make a thread object

def start():
    thread1.start()


def connecter():#a function that will connect signals

    QtCore.QObject.connect(ui.button, QtCore.SIGNAL("clicked()"),
        start)#connect the button when clicked with the start function

    QtCore.QObject.connect(thread1, QtCore.SIGNAL("anysignalname(bool)"),
        ui.changetext)#connect the thread1 object with the changetext function with the "anysignalname" signal that sends a bool value

ui.dialog.show()#show the dialog

connecter()#connect signals

ui.app.exec_()#start the app main loop


