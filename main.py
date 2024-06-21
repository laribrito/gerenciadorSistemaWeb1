from PyQt5 import QtWidgets
import sys
from classes import System
from controlers import Principal
from controlers.advanced import Advanced 

# por causa da atualização dos terminais
import os
os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    Sy = System()

    janelaPrincipal = Principal(Sy.getIp())
    
    janelaPrincipal.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
