import sys
import sqlite3

import easygui
import pandas as pd

from PyQt5 import QtWidgets, uic


class Ui(QtWidgets.QMainWindow):
    # Загрузка базы даных
    db = ''
    cursor = ''
    data_base = []
    table_names = []

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('..//ui//UI_Form.ui', self)

        # Список команд
        self.com_listWidget = self.findChild(QtWidgets.QListWidget, 'com_listWidget')

        # Список таблиц
        self.table_listWidget = self.findChild(QtWidgets.QListWidget, 'table_listWidget')

        # Текущая выбранная таблица
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Заголовок 1', 'Заголовок 2', 'Заголовок 3'])

        # Кнопка "Открыть БД"
        self.loadButton = self.findChild(QtWidgets.QPushButton, 'loadButton')
        self.loadButton.clicked.connect(self.load_db)

        # Кнопка "Выбрать"
        self.selectButton = self.findChild(QtWidgets.QPushButton, 'selectButton')
        self.selectButton.clicked.connect(self.select)

        self.show()

    def select(self):
        sel_items = self.table_listWidget.selectedItems()

        ind = 0
        for item in sel_items:
            ind = self.table_names.index(item.text())

        self.tableWidget.setColumnCount(len(self.data_base[ind].values[1]))
        self.tableWidget.setRowCount(len(self.data_base[ind].values[:]))
        r, c = 0, 0
        for item in self.data_base[ind].values[:]:
            c = 0
            for elem in item:
                info = QtWidgets.QTableWidgetItem(elem)
                self.tableWidget.setItem(r, c, info)
                c += 1
            r += 1
        self.tableWidget.setHorizontalHeaderLabels(self.data_base[ind].columns[:])
        # self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.resizeColumnsToContents()

    def load_db(self):
        # Выбор таблицы
        self.db = sqlite3.connect(easygui.fileopenbox())
        self.cursor = self.db.cursor()

        # Получение имен таблиц
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for table in self.cursor.fetchall():
            self.table_names.append(table[0])
        table_names = tuple(self.table_names)

        # Получение информации из базы данных
        for table in table_names:
            command = 'SELECT * FROM ' + table
            self.data_base.append(pd.read_sql_query(command, self.db))
            self.table_listWidget.addItem(table)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
    return


if __name__ == '__main__':
    main()