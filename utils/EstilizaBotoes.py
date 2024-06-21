def estilizaBotao(buttom):
    # Estilizando o botão com Qt Style Sheets
    buttom.setStyleSheet("""
        QPushButton {
            border-radius: 10px;
            background-color: #182e15;
            color: white;
            border: 1px solid rgb(255, 255, 255);
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
        }

        QPushButton:hover {
            background-color: #1f3a1c;
        }

        QPushButton:pressed {
            background-color: #152610;
            border-color: rgb(200, 200, 200);
        }
    """)
