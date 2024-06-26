import datetime
import subprocess
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5 import uic

from classes.SystemClass import System
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
        self.timer.start(1000)  # Atualiza a cada segundo

        # recuperar os botões
        allBtnsClicked = {
            'btnIniciarBack':   self.startBack, 
            'btnReiniciarBack': self.restartBack, 
            'btnDesligarBack':  self.stopBack,
            'btnIniciarFront':   self.startFront, 
            'btnReiniciarFront': self.restartFront, 
            'btnDesligarFront':  self.stopFront
        }

        for btnLabel, btnClicked in allBtnsClicked.items():
            btnObj = self.findChild(QPushButton, btnLabel)
            btnObj.clicked.connect(btnClicked)
            estilizaBotao(btnObj)

        # recuperar labels
        # status backend
        self.labelStatusBackend = self.findChild(QLabel, 'statusBackend')
        self.timer.timeout.connect(lambda : self.labelStatusBackend.setText(self._statusBack))

        # status frontend
        self.labelStatusFrontend = self.findChild(QLabel, 'statusFrontend')
        self.timer.timeout.connect(lambda : self.labelStatusFrontend.setText(self._statusFront))

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
        def trackerStatusFront(out):
            if 'Quit the server with CTRL-BREAK.' in out:
                self._statusFront = 'Ligado'
            elif 'Traceback' in out or 'Error' in out:
                self._statusFront = 'Error'
            elif 'Creating an optimized production build ...' in out:
                self._statusFront = 'Ligando'
            elif 'Serviço interrompido' in out:
                self._statusFront = 'Desligado'

        self._pastaFront = r'C:\Users\danie\OneDrive\Documents\programas\sistemaWeb1\front\frontendSistema'

        self._frontendTerminal = TerminalWidget(
            'terminalFrontend', 
            self._pastaFront, 
            ['npm.cmd', 'run', 'start'], 
            trackerStatusFront,
            self
        )

        self._statusFront = Advanced._possibleStatus[0]

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
        self._statusFront = 'Ligando'
        self._preparacaoFront()
        self._frontendTerminal.start()

    def restartFront(self):
        self._frontendTerminal.restart()
    
    def stopFront(self):
        self._frontendTerminal.stop()

    def getStatusFront(self):
        return self._statusFront
    
    def _preparacaoFront(self):
        self._fazStash()
        self._trocaParaBranchMain()
        self._atualizaIpNoSistema()
        self._preparaPastasParaLigarOSistema()
    
    def _fazStash(self):
        # guarda o que tiver de alteração não salva
        subprocess.run(['git', 'stash', '--include-untracked'], cwd=self._pastaFront)

    def _trocaParaBranchMain(self):
        # troca para a branch main
        subprocess.run(['git', 'checkout', 'main'], cwd=self._pastaFront)

    def _atualizaIpNoSistema(self):
        # Define o caminho do arquivo
        arquivo = f"{self._pastaFront}\\src\\services\\servers\\apiMainUrls.ts"

        # Define a nova linha
        port = '${port}/api' 
        nova_linha = f'export const API_ROOT = `http://{System().getIp()}:{port}`\n'

        # Lê o conteúdo do arquivo original
        with open(arquivo, 'r') as file:
            linhas = file.readlines()

        # Insere a nova linha no lugar desejado
        linhas[1] = (nova_linha)  # Insere na segunda posição (índice 1)

        # Escreve o conteúdo modificado de volta ao arquivo
        with open(arquivo, 'w') as file:
            file.writelines(linhas)

        # salvar as alterações do ip
        subprocess.run(['git', 'add', arquivo], cwd=self._pastaFront)

        subprocess.run(["git", "commit", "-m", fr"fix: atualiza ip {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"], cwd=self._pastaFront)

    def _preparaPastasParaLigarOSistema(self):
        # apaga as pastas preexistentes para  não dar erro de tipagem
        pastasApagar = ['build', 'dev']
        for i in pastasApagar:
            pasta_norm = os.path.normpath(rf'{self._pastaFront}/{i}')
            subprocess.run(['rmdir', '/s', '/q', pasta_norm], shell=True)