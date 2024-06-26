import socket

class System:
    _pastaFront = r'C:\Users\danie\OneDrive\Documents\programas\sistemaWeb1\front\frontendSistema'

    def __init__(self):
        self._ip = self._getCurrentIp()
        self.principalScreen = None

    def getIp(self):
        return self._ip
        
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
        # apaga as pastas preexistentes para  não dar erro de tipagem
        # pastasApagar = ['build', 'dev']
        # for i in pastasApagar:
        #     pasta_norm = os.path.normpath(rf'{System._pastaFront}/{i}')
        #     subprocess.run(['rmdir', '/s', '/q', pasta_norm], shell=True)
    