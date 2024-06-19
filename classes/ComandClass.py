class Comand:
    def __init__(self, comand, context, onActive=None) -> None:
        self.comand = comand
        self.context = context
        self.onActive = onActive