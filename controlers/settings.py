import os

# Obtém o caminho absoluto do diretório deste script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho para o diretório das telas
FOLDER_TO_SCREENS = os.path.join(SCRIPT_DIR, '..', 'telas')

# Caminho para o diretório dos arquivos estáticos
FOLDER_TO_STATICS = os.path.join(SCRIPT_DIR, '..', 'statics')
