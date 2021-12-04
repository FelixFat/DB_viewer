import os
import sys
import sqlite3

from PyQt5 import QtWidgets, uic

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('..//ui//UI_Form.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton') # Find the button
        self.button.clicked.connect(self.printButtonPressed) # Remember to pass the definition/method, not the return value!

        self.show()

    def printButtonPressed(self):
        pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
    return


if __name__ == '__main__':
    main()