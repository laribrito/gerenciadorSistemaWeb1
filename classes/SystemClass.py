import subprocess
import datetime
import socket
import os

class System:
    _possibleStates = ['Ligado', 'Desligado']

    def __init__(self):
        self._pastaFront = r'C:\Users\danie\OneDrive\Documents\programas\sistemaWeb1\front\frontendSistema'
        self._status = 'Desligado'
        self._ip = None

        self._getCurrentIp()

    def _getCurrentIp(self):
        # Obtém o endereço IP local
        # Obtém o nome do host da máquina
        host_name = socket.gethostname()

        # Obtém o endereço IP associado ao nome do host
        ip = socket.gethostbyname(host_name)

        # Remove espaços em branco no início e no final do endereço IP
        ip = ip.strip()

        self._ip = ip

    def _fazStash(self):
        # guarda o que tiver de alteração não salva
        subprocess.run(['git', 'stash', '--include-untracked'], cwd=self._pastaFront)

    def _trocaParaBranchMain(self):
        # troca para a branch main
        subprocess.run(['git', 'checkout', 'main'], cwd=self._pastaFront)

    def _atualizaIpNoSistema(self):
        if not self._ip:
            raise Exception('Não é possível atualizar o endereço de ip no sistema sem ter essa informação')

        # Define o caminho do arquivo
        arquivo = f"{self._pastaFront}\src\services\servers\apiMainUrls.ts"

        # Define a nova linha
        port = '${port}/api' 
        nova_linha = f'const API_ROOT = `http://{self._ip}:{port}`\n'

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
        # apaga as pastas preexistentes para não dar erro de tipagem
        pastasApagar = ['build', 'dev']
        for i in pastasApagar:
            pasta_norm = os.path.normpath(rf'{self._pastaFront}/{i}')
            subprocess.run(['rmdir', '/s', '/q', pasta_norm], shell=True)

    @property
    def ip(self):
        return self._ip
    
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, valor):
        # Verifica se o valor é uma string e está na lista permitida
        if isinstance(valor, str) and valor in System._possibleStates:
            self._status = valor
        else:
            raise ValueError(f"Valor inválido para status: {valor}. Deve ser uma string entre {System._possibleStates}.")