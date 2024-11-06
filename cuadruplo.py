# cuadruplo.py

class Cuadruplo:
    def __init__(self, operador, operando1, operando2, resultado):
        self.operador = operador
        self.operando1 = operando1
        self.operando2 = operando2
        self.resultado = resultado

    def __str__(self):
        return f"({self.operador}, {self.operando1}, {self.operando2}, {self.resultado})"
