from PyQt5 import QtWidgets
import sys
from classes import System
from controlers import Principal
from controlers.advanced import Advanced 

def main():
    app = QtWidgets.QApplication(sys.argv)
    Sy = System()

    janelaPrincipal = Principal(Sy.getIp())
    
    janelaAvancada = Advanced()
    
    janelaPrincipal.setScreenAdvanced(janelaAvancada)

    Sy.configs(janelaPrincipal, janelaAvancada)
    
    janelaPrincipal.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
