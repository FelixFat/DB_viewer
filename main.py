from PyQt5 import QtWidgets, uic
import sys

def main():
    app = QtWidgets.QApplication([])
    win = uic.loadUi('UI_Form.ui')  # расположение вашего файла .ui

    win.show()
    sys.exit(app.exec())

    return

if __name__ == '__main__':
    main()