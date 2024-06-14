import os
from PyQt5 import uic, QtWidgets
from controlers import FOLDER_TO_SCREENS

class Principal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing Principal")
        ui_file = os.path.join(FOLDER_TO_SCREENS, 'home.ui')
        uic.loadUi(ui_file, self)
        print("UI Loaded")
        self.show()
        print("Window Shown")
