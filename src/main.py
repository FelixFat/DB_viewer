import os
import sys
import sqlite3


from PyQt5 import QtWidgets, uic


def main():
    path_ui = os.getcwd()[:-4] + '\\ui\\UI_Form.ui'
    path_db = os.getcwd()[:-4] + '\\Study_session.db'

    app = QtWidgets.QApplication([])
    win = uic.loadUi(path_ui)

    ###
    
    db = sqlite3.connect(path_db)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Студенты')

    table_db = cursor.fetchall()

    ###

    win.show()
    sys.exit(app.exec())

    return

if __name__ == '__main__':
    main()
