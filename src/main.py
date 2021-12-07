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

    req = (
        'Студенты с оценками 4 и 5',
        'Студенты получившие зачет',
        'Студенты не получившие зачет'
    )
    req_db = []

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

        # Кнопка "Выбрать" для списка таблиц
        self.selectButton = self.findChild(QtWidgets.QPushButton, 'selectButton')
        self.selectButton.clicked.connect(self.select)

        # Кнопка "Выбрать" для списка команд
        self.selectButton_2 = self.findChild(QtWidgets.QPushButton, 'selectButton_2')
        self.selectButton_2.clicked.connect(self.select_2)

        # Кнопка "Открыть БД"
        self.loadButton = self.findChild(QtWidgets.QPushButton, 'loadButton')
        self.loadButton.clicked.connect(self.load_db)

        # Кнопка "Сохранить ДБ" для списка команд
        self.saveButton = self.findChild(QtWidgets.QPushButton, 'saveButton')
        self.saveButton.clicked.connect(self.save_db)

        self.show()

        return

    # Кнопка "Выбрать" для списка таблиц
    def select(self):
        try:
            sel_items = self.table_listWidget.selectedItems()

            ind = 0
            for item in sel_items:
                ind = self.table_names.index(item.text())

            row = len(self.data_base[ind].values[:])
            col = len(self.data_base[ind].values[1])
            self.tableWidget.setColumnCount(col)
            self.tableWidget.setRowCount(row)
            for i in range(row):
                for j in range(col):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(self.data_base[ind].values[i][j]))
            self.tableWidget.setHorizontalHeaderLabels(self.data_base[ind].columns[:])
            self.tableWidget.resizeColumnsToContents()
        except:
            print('Error "select"')

        return

    # Кнопка "Выбрать" для списка команд
    def select_2(self):
        try:
            sel_items = self.com_listWidget.selectedItems()

            ind = -1
            for item in sel_items:
                ind = self.req.index(item.text())

            if ind == 0:
                self.cursor.execute('SELECT "Студенты"."Шифр студента", "Студенты"."Фамилия", "Экзамены"."Шифр дисциплины", "Дисциплины"."Название дисциплины", "Экзамены"."Оценка"\n' +
                                    'FROM "Студенты", "Экзамены", "Дисциплины"\n' +
                                    'WHERE "Студенты"."Шифр студента" == "Экзамены"."Шифр студента" AND "Экзамены"."Шифр дисциплины" == "Дисциплины"."Шифр дисциплины" AND ("Экзамены"."Оценка" == "хор" OR "Экзамены"."Оценка" == "отл")\n' +
                                    'ORDER BY "Студенты"."Шифр студента"\n' +
                                    ';')
            elif ind == 1:
                self.cursor.execute('SELECT "Студенты"."Шифр студента", "Студенты"."Фамилия", "Зачеты"."Шифр дисциплины", "Дисциплины"."Название дисциплины", "Зачеты"."Зачет"' +
                                    'FROM "Студенты", "Зачеты", "Дисциплины"' +
                                    'WHERE "Студенты"."Шифр студента" == "Зачеты"."Шифр студента" AND "Зачеты"."Шифр дисциплины" == "Дисциплины"."Шифр дисциплины" AND "Зачеты"."Зачет" == "зачтено"' +
                                    'ORDER BY "Студенты"."Шифр студента"' +
                                    ';')
            elif ind == 2:
                self.cursor.execute('SELECT "Студенты"."Шифр студента", "Студенты"."Фамилия", "Зачеты"."Шифр дисциплины", "Дисциплины"."Название дисциплины", "Зачеты"."Зачет"' +
                                    'FROM "Студенты", "Зачеты", "Дисциплины"' +
                                    'WHERE "Студенты"."Шифр студента" == "Зачеты"."Шифр студента" AND "Зачеты"."Шифр дисциплины" == "Дисциплины"."Шифр дисциплины" AND "Зачеты"."Зачет" == "не зачтено"' +
                                    'ORDER BY "Студенты"."Шифр студента"' +
                                    ';')

            self.req_db = self.cursor.fetchall()

            row = len(self.req_db)
            col = len(self.req_db[1])
            self.tableWidget.setColumnCount(col)
            self.tableWidget.setRowCount(row)
            for i in range(len(self.req_db)):
                for j in range(len(self.req_db[1])):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(self.req_db[i][j]))
            self.tableWidget.setHorizontalHeaderLabels(['1', '2', '3', '4', '5'])
            self.tableWidget.resizeColumnsToContents()
        except :
            print('Error "select_2"')

        return

    # Кнопка "Открыть БД"
    def load_db(self):
        try:
            # Выбор таблицы
            file = easygui.fileopenbox()
            self.db = sqlite3.connect(file)
            self.cursor = self.db.cursor()

            if file[file.rfind('\\') + 1:] == 'Study_session.db':
                for item in self.req:
                    self.com_listWidget.addItem(item)

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
        except:
            print('Error "load_db"')

        return

    def save_db(self):
        try:
            dir = easygui.diropenbox()
            new_db = sqlite3.connect(dir + '\\result.db')
            cur = new_db.cursor()

            try:
                cur.execute('CREATE TABLE result (c1 text, c2 text, c3 text, c4 text, c5 text);')
            except:
                cur.execute('DROP TABLE result')
                cur.execute('CREATE TABLE result (c1 text, c2 text, c3 text, c4 text, c5 text);')

            cur.executemany('INSERT INTO result VALUES(?, ?, ?, ?, ?);', self.req_db)
            new_db.commit()
        except:
            print('Error "save_db"')

        return


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()

    return


if __name__ == '__main__':
    main()