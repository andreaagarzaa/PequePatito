# pilas_cuadruplos.py

class PilasCuadruplos:
    def __init__(self):
        self.pila_operadores = []
        self.pila_operandos = []
        self.pila_tipos = []
        self.pila_saltos = []

    def push_operador(self, operador):
        self.pila_operadores.append(operador)

    def pop_operador(self):
        if self.pila_operadores:
            return self.pila_operadores.pop()
        return None

    def push_operando(self, operando):
        self.pila_operandos.append(operando)

    def pop_operando(self):
        if self.pila_operandos:
            return self.pila_operandos.pop()
        return None

    def push_tipo(self, tipo):
        self.pila_tipos.append(tipo)

    def pop_tipo(self):
        if self.pila_tipos:
            return self.pila_tipos.pop()
        return None

    def push_salto(self, salto):
        self.pila_saltos.append(salto)
        print(f"Push a pila_saltos: {salto}. Estado actual: {self.pila_saltos}")

    def pop_salto(self):
        if self.pila_saltos:
            salto = self.pila_saltos.pop()
            print(f"Pop de pila_saltos: {salto}. Estado actual: {self.pila_saltos}")
            return salto
        else:
            print("Intento de pop en pila_saltos vacía")
            return None

    def pop_salto_indice(self, indice):
        return self.pila_saltos.pop(indice)