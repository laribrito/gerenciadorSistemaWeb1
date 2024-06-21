import subprocess
import datetime
import socket
import os
from controlers import Principal
from controlers.advanced import Advanced 
from PyQt5.QtCore import QTimer
import time

class System:
    _pastaFront = r'C:\Users\danie\OneDrive\Documents\programas\sistemaWeb1\front\frontendSistema'
    _pastaBack = r'C:\Users\danie\OneDrive\Documents\programas\sistemaWeb1\back\backendSistema'
    _ip = None

    def __init__(self):
        self._ip = self._getCurrentIp()
        self.principalScreen = None

    def setPrincipalScreen(self, screen:Principal):
        self.principalScreen = screen

    def setAdvancedScreen(self, screen:Advanced):
        self.advancedScreen = screen

    def getIp(self):
        return self._ip
    
    def configs(self, principal, avancada):
        self.setPrincipalScreen(principal)
        self.setAdvancedScreen(avancada)

        # Atualiza o status do sistema principal periodicamente
        self.timer = QTimer(self.principalScreen)
        self.timer.timeout.connect(self.atualizarStatus)
        self.timer.start(1000)  # Atualiza a cada segundo

        # adiciona funções nos botões da tela principal
        # TELA PRINCIPAL

        # BOTÃO INICIAR
        self.principalScreen.realActionIniciar = self.iniciarTelaPrincipal

        # BOTÃO DESLIGAR
        self.principalScreen.realActionDesligar = self.desligarTelaPrincipal

        # BOTÃO REINICIAR
        self.principalScreen.realActionReiniciar = self.reiniciarTelaPrincipal

    def iniciarTelaPrincipal(self):
        self.iniciarBackend()

    def desligarTelaPrincipal(self):
        self.desligarBackend()

    def reiniciarTelaPrincipal(self):
        self.reiniciarBackend()

    def atualizarStatus(self):
        statusBack = self.advancedScreen.getStatusBack()
        statusFront = self.advancedScreen.getStatusFront()

        if statusFront == 'Error' or statusBack == 'Error':
            self.principalScreen.setStatusSystem("Erro")
        elif statusFront == 'Ligando' or statusBack == 'Ligando':
            self.principalScreen.setStatusSystem("Ligando")
        elif statusFront == 'Ligado' and statusBack == 'Ligado':
            self.principalScreen.setStatusSystem("Ligado")
        else:
            self.principalScreen.setStatusSystem("Desligado")
    
    def iniciarBackend(self):
        self.advancedScreen.backendTerminal.startServer()
        
    def desligarBackend(self):
        self.advancedScreen.backendTerminal.stopServer()

    def reiniciarBackend(self):
        self.advancedScreen.backendTerminal.restart()
        
    @staticmethod
    def _getCurrentIp():
        # Obtém o endereço IP local
        # Obtém o nome do host da máquina
        host_name = socket.gethostname()

        # Obtém o endereço IP associado ao nome do host
        ip = socket.gethostbyname(host_name)

        # Remove espaços em branco no início e no final do endereço IP
        ip = ip.strip()

        return ip

    # @staticmethod
    # def _preparacaoFront():
    #     System._fazStash()
    #     System._trocaParaBranchMain()
    #     System._atualizaIpNoSistema()
    #     System._preparaPastasParaLigarOSistema()
 
    # async def iniciarFrontend(self):
    #     # System._preparacaoFront()
    #     self.principalScreen.setTextlabelToSendStatus('Começõu')
    
    # @staticmethod
    # def _fazStash():
    #     # guarda o que tiver de alteração não salva
    #     subprocess.run(['git', 'stash', '--include-untracked'], cwd=System._pastaFront)

    # @staticmethod
    # def _trocaParaBranchMain():
    #     # troca para a branch main
    #     subprocess.run(['git', 'checkout', 'main'], cwd=System._pastaFront)

    # @staticmethod
    # def _atualizaIpNoSistema():
    #     if not System._ip:
    #         raise Exception('Não é possível atualizar o endereço de ip no sistema sem ter essa informação')

    #     # Define o caminho do arquivo
    #     arquivo = f"{System._pastaFront}\src\services\servers\apiMainUrls.ts"

    #     # Define a nova linha
    #     port = '${port}/api' 
    #     nova_linha = f'const API_ROOT = `http://{System._ip}:{port}`\n'

    #     # Lê o conteúdo do arquivo original
    #     with open(arquivo, 'r') as file:
    #         linhas = file.readlines()

    #     # Insere a nova linha no lugar desejado
    #     linhas[1] = (nova_linha)  # Insere na segunda posição (índice 1)

    #     # Escreve o conteúdo modificado de volta ao arquivo
    #     with open(arquivo, 'w') as file:
    #         file.writelines(linhas)

    #     # salvar as alterações do ip
    #     subprocess.run(['git', 'add', arquivo], cwd=System._pastaFront)

    #     subprocess.run(["git", "commit", "-m", fr"fix: atualiza ip {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"], cwd=System._pastaFront)

    # @staticmethod
    # def _preparaPastasParaLigarOSistema():
        # apaga as pastas preexistentes para não dar erro de tipagem
        # pastasApagar = ['build', 'dev']
        # for i in pastasApagar:
        #     pasta_norm = os.path.normpath(rf'{System._pastaFront}/{i}')
        #     subprocess.run(['rmdir', '/s', '/q', pasta_norm], shell=True)
    