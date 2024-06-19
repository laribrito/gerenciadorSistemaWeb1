from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5 import uic

from classes.ComandClass import Comand
from controlers import FOLDER_TO_SCREENS, FOLDER_TO_STATICS

import os

from widgets.Terminal import TerminalWidget

class Advanced(QMainWindow):
    _possibleStatesBack = ['Desligado', 'Ligado', 'Error', 'Ligando']

    def __init__(self):
        super().__init__()
        ui_file = os.path.join(FOLDER_TO_SCREENS, 'advanced.ui')
        uic.loadUi(ui_file, self)

        # ATRIBUTOS

        # COMPONENTES

        # recuperar os botões
        allBtnsClicked = {}

        for btnLabel, btnClicked in allBtnsClicked.items():
            btnObj = self.findChild(QPushButton, btnLabel)
            btnObj.clicked.connect(btnClicked)
            self.estilizaBotao(btnObj)

        # recuperar labels
        # status backend
        self.labelStatusBackend = self.findChild(QLabel, 'statusBackend')

        # status frontend
        self.labelStatusFrontend = self.findChild(QLabel, 'statusFrontend')

        # Atualiza a label periodicamente
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.attStatusBack)
        self.timer.start(1000)  # Atualiza a cada segundo

        # BACKEND
        self._backendTerminal = TerminalWidget('terminalBackend', self)
        self._statusBack = Advanced._possibleStatesBack[0]

        # FRONTEND
        self._statusFront = 'Ligado'

    def attStatusBack(self):
        self.labelStatusBackend.setText(self._statusBack)

    def attStatusFront(self):
        self.labelStatusBackend.setText(self._statusFront)

    def getStatusBack(self):
        return self._statusBack
    
    def getStatusFront(self):
        return self._statusFront

    def executeComandBack(self, command:Comand):
        self._backendTerminal.executar_comando(command.comand, command.context, command.onActive)

    def finishBack(self):
        self._backendTerminal.parar_comando()
        self.setStatusBack('Desligado')

    def reiniciarBack(self, command:Comand):
        self._backendTerminal.reiniciar(command.comand, command.context, command.onActive)

    def setStatusBack(self, status):
        if status in Advanced._possibleStatesBack:
            self._statusBack = status

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
