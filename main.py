import sys

# Pqt5
from PyQt5.QtWidgets import QDialog,QApplication, QMainWindow, QHeaderView, QFileDialog
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets

# Local
from gui import MainWindow



def run():
    app = QApplication(sys.argv)
    my_app = MainWindow()
    my_app.show()
    my_app.test_data()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()