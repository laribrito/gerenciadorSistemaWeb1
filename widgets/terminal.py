import datetime
from PyQt5.QtWidgets import QWidget, QTextEdit
from PyQt5.QtCore import pyqtSignal, QObject
import subprocess
import threading
import psutil

class ServiceThread(threading.Thread, QObject):
    output_signal = pyqtSignal(str)  # Sinal para enviar a saída do subprocesso
    TAM_LINE = 20

    def __init__(self, path, comandList):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.path = path
        self.process = None
        self.stdout_thread = None
        self.stderr_thread = None
        self.comandList = comandList
        self._stop_event = threading.Event()

    def run(self):
        # Iniciar o servidor Django
        self.process = subprocess.Popen(
            self.comandList,
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        # print("Servidor Django iniciado...")  # Depuração
        self.output_signal.emit(f"\nServiço iniciado {'-'*ServiceThread.TAM_LINE} {self.getDate()} \n")

        # Threads para leitura de stdout e stderr
        stdout_thread = threading.Thread(target=self.read_stdout)
        stderr_thread = threading.Thread(target=self.read_stderr)

        stdout_thread.start()
        stderr_thread.start()

    def read_stdout(self):
        for line in iter(self.process.stdout.readline, ''):
            if self._stop_event.is_set():
                break
            # line = line.strip()
            if line:
                print(f"Emitting output: {line.encode('utf-8')}")  # Depuração
                self.output_signal.emit(line)

        if self.process:
            self.process.stdout.close()

    def read_stderr(self):
        for line in iter(self.process.stderr.readline, ''):
            if self._stop_event.is_set():
                break
            # line = line.strip()
            if line:
                # print(f"Emitting error: {line}")  # Depuração
                self.output_signal.emit(line)

        if self.process:
            self.process.stderr.close()

    def getDate(self):
        # Obtém a data atual
        current_datetime = datetime.datetime.now()
        
        # Retorna a data atual no formato desejado
        return current_datetime.strftime('%d / %m / %Y %H:%M:%S') + '-' * ServiceThread.TAM_LINE

    def stop_server(self):
        if self.process:
            # Parar threads de leitura se ainda estiverem em execução
            if self.stdout_thread and self.stdout_thread.is_alive():
                self.stdout_thread.join()
            if self.stderr_thread and self.stderr_thread.is_alive():
                self.stderr_thread.join()

            # Terminar o processo e seus filhos
            process = psutil.Process(self.process.pid)
            for proc in process.children(recursive=True):
                proc.terminate()
            process.terminate()
            self.process = None
            self.output_signal.emit(f"\nServiço interrompido {'-'*(ServiceThread.TAM_LINE-7)} {self.getDate()}\n") 
            # print(f"Serviço interrompido {'-'*ServiceThread.TAM_LINE}")  # Depuração

    def stop(self):
        self._stop_event.set()
        self.stop_server()

class TerminalWidget(QWidget):
    def __init__(self, labelComponent, cwd, comandList, trackerStatus, parent):
        super().__init__(parent)

        self.text_edit = parent.findChild(QTextEdit, labelComponent)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                font-size: 10pt;
                background-color: black;
                color: white;
            }
        """)

        self.path = cwd
        self.comandList = comandList
        self.server_thread = None
        self.tracker = trackerStatus

    def start(self):
        self.server_thread = ServiceThread(self.path, self.comandList)
        self.server_thread.output_signal.connect(self.update_text_edit)
        self.server_thread.start()

    def stop(self):
        if self.server_thread:
            self.server_thread.stop()

    def restart(self):
        self.stop()
        self.start()

    def clean_terminal_output(self, text):
        import re
        
        # Expressão regular para remover códigos de escape ANSI
        print('texto antes: ', text)
        
        # Padrão regex para o formato \xhh
        padrao_hex = r'\\x[0-9a-fA-F]{2}'
        
        # Padrão regex para caracteres estranhos
        padrao_estranho = r'[^\x00-\x7F]+'

        padroes = [padrao_hex, padrao_estranho]

        for padrao in padroes:
            cleaned_text = re.sub(padrao, '', text)

        print('text depois: ', cleaned_text)

        return cleaned_text
    
    def update_text_edit(self, text):
        text = self.clean_terminal_output(text)
        print(text)
        self.text_edit.append(text)

        if self.tracker:
            self.tracker(text)
