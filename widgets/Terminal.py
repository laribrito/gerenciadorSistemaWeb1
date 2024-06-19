from PyQt5.QtWidgets import QTextEdit, QWidget
from PyQt5.QtCore import QProcess

class TerminalWidget(QWidget):
    def __init__(self, labelComponent, parent):
        super().__init__(parent)

        self.customViewOutput = None

        self.text_edit = parent.findChild(QTextEdit, labelComponent)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                font-size: 10pt; /* Tamanho da fonte */
                background-color: black; /* Fundo preto */
                color: white; /* Texto branco */
            }
        """)

        # self.run_button.clicked.connect(self.executar_comando)
        # self.stop_button.clicked.connect(self.parar_comando)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.on_ready_read_stdout)
        self.process.readyReadStandardError.connect(self.on_ready_read_stderr)

    def executar_comando(self, comand, context, viewOutput=None):
        # Define o diretório de trabalho (contexto) para o comando
        self.process.setWorkingDirectory(context)

        # Inicia o processo com o comando e argumentos especificados
        self.process.start(comand)

        if viewOutput:
            self.customViewOutput = viewOutput

    def reiniciar(self, comand, context, viewOutput=None):
        self.process.kill()

        self.executar_comando(comand, context, viewOutput)

    def parar_comando(self):
        # Termina o processo em execução
        self.process.kill()
        self.text_edit.append("Processo interrompido.")

    def on_ready_read_stdout(self):
        # Lê a saída padrão do processo e adiciona ao QTextEdit
        output = self.process.readAllStandardOutput().data().decode('utf-8')
        self.text_edit.append(output)

        if self.customViewOutput:
            self.customViewOutput(output, self.text_edit)

    def on_ready_read_stderr(self):
        # Lê a saída de erro do processo e adiciona ao QTextEdit
        error = self.process.readAllStandardError().data().decode('utf-8')
        self.text_edit.append(error)

        if self.customViewOutput:
            self.customViewOutput(error, self.text_edit)
