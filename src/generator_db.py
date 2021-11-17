import sqlite3
import pandas as pd
import random


def generation():
    # Загрузка базы даных
    db = sqlite3.connect('Study_session.db')
    cursor = db.cursor()

    # Получение имен таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = []
    for table in cursor.fetchall():
        table_names.append(table[0])
    table_names = tuple(table_names)

    # Получение информации из базы данных
    data_base = []
    for table in table_names:
        command = 'SELECT * FROM ' + table
        data_base.append(pd.read_sql_query(command, db))

    # Заполнение пустых таблиц
    date = ('01.05.2021', '05.05.2021', '10.05.2021', '16.05.2021', '20.05.2021')
    grade_zach = ('не зачтено', 'зачтено')
    grade_ekz = ('не оценено', 'удовл', 'хор', 'отл')

    for student in data_base[2].values[:]:
        for subject in data_base[0].values[:4]:
            d_i = random.randint(0, len(date) - 1)
            g_i = random.randint(0, len(grade_zach) - 1)
            inp = pd.Series([student[0], date[d_i], subject[0], grade_zach[g_i]], index=data_base[1].columns)
            data_base[1] = data_base[1].append(inp, ignore_index=True)

    for student in data_base[2].values[:]:
        for subject in data_base[0].values[4:]:
            d_i = random.randint(0, len(date) - 1)
            g_i = random.randint(0, len(grade_ekz) - 1)
            inp = pd.Series([student[0], date[d_i], subject[0], grade_ekz[g_i]], index=data_base[3].columns)
            data_base[3] = data_base[3].append(inp, ignore_index=True)

    inp_1 = []
    inp_2 = []
    for i in data_base[1].values[:]: inp_1.append([i[0], i[1], i[2], i[3]])
    for i in data_base[3].values[:]: inp_2.append([i[0], i[1], i[2], i[3]])
    cursor.executemany('INSERT INTO Зачеты VALUES(?, ?, ?, ?);', inp_1)
    cursor.executemany('INSERT INTO Экзамены VALUES(?, ?, ?, ?);', inp_2)
    #db.commit()

    return
