from controlers import FOLDER_TO_SCREENS
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
import os

class Principal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing Principal")
        ui_file = os.path.join(FOLDER_TO_SCREENS, 'home.ui')
        uic.loadUi(ui_file, self)
        print("UI Loaded")
        self.show()
        print("Window Shown")

        # recuperar os botões
        allBtnsClicked = {
            'btnIniciar':   self.actionIniciar, 
            'btnReiniciar': self.actionReiniciar, 
            'btnDesligar':  self.actionDesligar
        }

        for btnLabel, btnClicked in allBtnsClicked.items():
            btnObj = self.findChild(QtWidgets.QPushButton, btnLabel)
            btnObj.clicked.connect(btnClicked)
            self.estilizaBotao(btnObj)

        # configurar label que leva para a tela avançada
        labelAvancadas = self.findChild(QtWidgets.QLabel, 'labelAvancadas')
        labelAvancadas.mousePressEvent = self.actionLabelAvancadas

    def estilizaBotao(self, buttom):
        # Estilizando o botão com Qt Style Sheets
        buttom.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: #182e15;
                color: white;
                border: 1px solid rgb(255, 255, 255);
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }

            QPushButton:hover {
                background-color: #1f3a1c;
            }

            QPushButton:pressed {
                background-color: #152610;
                border-color: rgb(200, 200, 200);
            }
        """)

    def actionLabelAvancadas(self, event):
        if event.button() == Qt.LeftButton:
            QtWidgets.QMessageBox.information(self, "Título da Caixa de Diálogo", "ação de avançadas")

    def actionIniciar(self):
        QtWidgets.QMessageBox.information(self, "Título da Caixa de Diálogo", "ação de iniciar")

    def actionReiniciar(self):
        QtWidgets.QMessageBox.information(self, "Título da Caixa de Diálogo", "ação de reiniciar")

    def actionDesligar(self):
        QtWidgets.QMessageBox.information(self, "Título da Caixa de Diálogo", "ação de desligar")
