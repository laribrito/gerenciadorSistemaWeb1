import sys
import os

from controlers.advanced import Advanced
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QPushButton, \
    QLabel, QMessageBox
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic

from settings import FOLDER_TO_SCREENS, FOLDER_TO_STATICS

import os

class Principal(QMainWindow):
    def __init__(self, ipAddress):
        super().__init__()
        print("Initializing Principal")
        ui_file = os.path.join(FOLDER_TO_SCREENS, 'home.ui')
        uic.loadUi(ui_file, self)
        print("UI Loaded")
        self.show()
        print("Window Shown")

        # ATRIBUTOS
        self._systemMainAddress = ''
        self._systemAdminAddress = ''
        self.advancedScreen = None
        self.realActionIniciar = None
        self.realActionDesligar = None
        self.realActionReiniciar = None
        self._statusSystem = 'Desligado'

        # COMPONENTES
        # componente de área de transferência
        self.clipboardObj = QGuiApplication.clipboard()

        # componente para sistema de notificações
        self.notificationsObj = QSystemTrayIcon(self)
        self.notificationsObj.setIcon(QIcon(os.path.join(FOLDER_TO_STATICS, 'logo.png')))  # Substitua pelo caminho do seu ícone
        self.notificationsObj.setVisible(True)
        self.notificationsObj.show()

        # recuperar os botões
        allBtnsClicked = {
            'btnIniciar':   self.actionIniciar, 
            'btnReiniciar': self.actionReiniciar, 
            'btnDesligar':  self.actionDesligar
        }

        for btnLabel, btnClicked in allBtnsClicked.items():
            btnObj = self.findChild(QPushButton, btnLabel)
            btnObj.clicked.connect(btnClicked)
            self.estilizaBotao(btnObj)

        # configurar label que leva para a tela avançada
        labelAvancadas = self.findChild(QLabel, 'labelAvancadas')
        labelAvancadas.mousePressEvent = self.actionLabelAvancadas

        # trocar o valor das variáveis
        self._systemMainAddress = ipAddress
        self._systemAdminAddress = f'{ipAddress}:8000'

        # configurar o label que exibe informação de status do sistema
        self.labelToSendStatus = self.findChild(QLabel, 'labelSystemStatus')
        self.labelToSendStatus.setText(self._statusSystem)

        # configura o label que exibe o endereço do sistema principal
        labelToSendSystemMain = self.findChild(QLabel, 'systemMainLabel')
        labelToSendSystemMain.mousePressEvent = self.actionLabelSystemMain
        labelToSendSystemMain.setText(f'Principal: {ipAddress}')

        # configura o label que exibe o endereço do sistema admin
        labelToSendSystemAdmin = self.findChild(QLabel, 'systemAdminLabel')
        labelToSendSystemAdmin.mousePressEvent = self.actionLabelSystemAdmin
        labelToSendSystemAdmin.setText(f'Admin: {ipAddress}:8000')

        # método que atualizará o status
        # Atualiza a label periodicamente
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setTextlabelToSendStatus)
        self.timer.start(1000)  # Atualiza a cada segundo

    def setTextlabelToSendStatus(self):
        self.labelToSendStatus.setText(self._statusSystem)

    def setScreenAdvanced(self, screen:Advanced):
        self.advancedScreen = screen

    def setStatusSystem(self, status):
        self._statusSystem = status

    def actionLabelSystemMain(self, event):
        if event.button() == Qt.LeftButton:
            self.actionCopyContentLabel(self._systemMainAddress)

    def actionLabelSystemAdmin(self, event):
        if event.button() == Qt.LeftButton:
            self.actionCopyContentLabel(self._systemAdminAddress)

    def actionCopyContentLabel(self, txt):
        self.clipboardObj.setText(txt)
        self.notificationsObj.showMessage(
            "Texto copiado com sucesso",
            None,
            QSystemTrayIcon.Information,
            3000 
        )

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
            if self.advancedScreen:
                self.advancedScreen.show()

    def actionIniciar(self):
        if self.realActionIniciar:
            self.realActionIniciar()

    def actionReiniciar(self):
        if self.realActionReiniciar:
            self.realActionReiniciar()

    def actionDesligar(self):
        if self.realActionDesligar:
            self.realActionDesligar()
