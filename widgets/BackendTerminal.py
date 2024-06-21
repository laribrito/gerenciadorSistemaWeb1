import os
import select
from PyQt5.QtWidgets import QWidget, QTextEdit
import subprocess
import threading
import psutil
import time

import threading
import subprocess
import time
import psutil
from PyQt5.QtCore import pyqtSignal, QObject


class DjangoServerThread(threading.Thread, QObject):
    output_signal = pyqtSignal(str)  # Sinal para enviar a saída do subprocesso

    def __init__(self, path):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.path = path
        self.process = None
        self.stdout_thread = None
        self.stderr_thread = None
        self._stop_event = threading.Event()

    def run(self):
        # Iniciar o servidor Django
        self.process = subprocess.Popen(
            ['python', 'manage.py', 'runserver', '0.0.0.0:8001'],
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        # print("Servidor Django iniciado...")  # Depuração
        self.output_signal.emit("Servidor Django iniciado...")

        # Threads para leitura de stdout e stderr
        stdout_thread = threading.Thread(target=self.read_stdout)
        stderr_thread = threading.Thread(target=self.read_stderr)

        stdout_thread.start()
        stderr_thread.start()

    def read_stdout(self):
        for line in iter(self.process.stdout.readline, ''):
            if self._stop_event.is_set():
                break
            line = line.strip()
            if line:
                # print(f"Emitting output: {line}")  # Depuração
                self.output_signal.emit(line)
        self.process.stdout.close()

    def read_stderr(self):
        for line in iter(self.process.stderr.readline, ''):
            if self._stop_event.is_set():
                break
            line = line.strip()
            if line:
                # print(f"Emitting error: {line}")  # Depuração
                self.output_signal.emit(line)
        self.process.stderr.close()

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
            # print("Servidor Django foi interrompido")  # Depuração
            self.output_signal.emit("Servidor Django foi interrompido")

    def stop(self):
        self._stop_event.set()
        self.stop_server()

class BackendTerminalWidget(QWidget):
    def __init__(self, labelComponent, parent):
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

        self.path = r'C:\Users\danie\OneDrive\Documents\programas\sistemaWeb1\back\backendSistema'
        self.server_thread = None

    def startServer(self):
        self.server_thread = DjangoServerThread(self.path)
        self.server_thread.output_signal.connect(self.update_text_edit)
        self.server_thread.start()

    def stopServer(self):
        self.server_thread.stop()

    def restart(self):
        self.stopServer()
        self.startServer()

    def update_text_edit(self, text):
        self.text_edit.append(text)
