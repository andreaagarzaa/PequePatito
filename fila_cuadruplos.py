# fila_cuadruplos.py

class FilaCuadruplos:
    def __init__(self):
        self.cuadruplos = []

    def agregar_cuadruplo(self, operador, op1, op2, resultado):
        cuadruplo = (operador, op1, op2, resultado)
        self.cuadruplos.append(cuadruplo)

    def imprimir_cuadruplos(self):
        print("==== Cuádruplos Generados ====")
        for idx, cuadruplo in enumerate(self.cuadruplos):
            operador, op1, op2, resultado = cuadruplo
            print(f"{idx}: ({operador}, {op1}, {op2}, {resultado})")
        print(f"{len(self.cuadruplos)}: (End of program)")
