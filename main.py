from PyQt5 import QtWidgets
import sys
from controlers import Principal 

def main():
    app = QtWidgets.QApplication(sys.argv)
    janela = Principal()
    janela.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
