import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5 import uic

from classes.ComandClass import Comand
from controlers import FOLDER_TO_SCREENS, FOLDER_TO_STATICS

import os

from utils.EstilizaBotoes import estilizaBotao
from widgets.terminal import TerminalWidget

class Advanced(QMainWindow):
    _possibleStatus = ['Desligado', 'Ligado', 'Error', 'Ligando']

    def __init__(self):
        super().__init__()
        ui_file = os.path.join(FOLDER_TO_SCREENS, 'advanced.ui')
        uic.loadUi(ui_file, self)

        # ATRIBUTOS

        # COMPONENTES
        self.timer = QTimer(self)

        # recuperar os botões
        allBtnsClicked = {
            'btnIniciarBack':   self.startBack, 
            'btnReiniciarBack': self.restartBack, 
            'btnDesligarBack':  self.stopBack
        }

        for btnLabel, btnClicked in allBtnsClicked.items():
            btnObj = self.findChild(QPushButton, btnLabel)
            btnObj.clicked.connect(btnClicked)
            estilizaBotao(btnObj)

        # recuperar labels
        # status backend
        self.labelStatusBackend = self.findChild(QLabel, 'statusBackend')
        self.timer.timeout.connect(lambda : self.labelStatusBackend.setText(self._statusBack))
        self.timer.start(1000)  # Atualiza a cada segundo

        # status frontend
        self.labelStatusFrontend = self.findChild(QLabel, 'statusFrontend')

        # Atualiza a label periodicamente
        self.timer = QTimer(self)
        # self.timer.timeout.connect(self.attStatusBack)
        self.timer.start(1000)  # Atualiza a cada segundo

        # BACKEND
        def trackerStatusBack(out):
            if 'Quit the server with CTRL-BREAK.' in out:
                self._statusBack = 'Ligado'
            elif 'Traceback' in out:
                self._statusBack = 'Error'
            elif 'Serviço iniciado' in out:
                self._statusBack = 'Ligando'
            elif 'Serviço interrompido' in out:
                self._statusBack = 'Desligado'

        self._backendTerminal = TerminalWidget(
            'terminalBackend', 
            r'C:\Users\danie\OneDrive\Documents\programas\sistemaWeb1\back\backendSistema', 
            ['python', 'manage.py', 'runserver', '0.0.0.0:8001'], 
            trackerStatusBack,
            self
        )

        self._statusBack = Advanced._possibleStatus[0]

        # FRONTEND
        self._statusFront = 'Ligado'

    # MÉTODOS BACKEND
    def startBack(self):
        self._backendTerminal.start()

    def restartBack(self):
        self._backendTerminal.restart()
    
    def stopBack(self):
        self._backendTerminal.stop()

    def setStatusBack(self, status):
        if status in Advanced._possibleStatus:
            self._statusBack = status

    def getStatusBack(self):
        return self._statusBack
    
    # MÉTODOS FRONT
    def startFront(self):
        return
        self._frontendTerminal.start()

    def restartFront(self):
        return
        self._frontendTerminal.restart()
    
    def stopFront(self):
        return
        self._frontendTerminal.stop()

    def setStatusFront(self, status):
        return
        if status in Advanced._possibleStatus:
            self._statusFront = status

    def getStatusFront(self):
        return self._statusFront