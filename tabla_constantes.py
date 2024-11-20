# tabla_constantes.py
class TablaConstantes:
    def __init__(self):
        self.constantes = {}  # {valor: dirección}
        self.contadores = {
            'entero': 10000,
            'flotante': 11000,
            'cadena': 12000,
            'booleano': 13000
        }

    def agregar_constante(self, valor, tipo):
        if valor not in self.constantes:
            direccion = self.contadores[tipo]
            self.constantes[valor] = direccion
            self.contadores[tipo] += 1
        return self.constantes[valor]

    def obtener_direccion(self, valor):
        return self.constantes.get(valor, None)

    def imprimir_constantes(self):
        print("==== Tabla de Constantes ====")
        for valor, direccion in self.constantes.items():
            print(f"Valor: {valor}, Dirección: {direccion}")
        print("=============================")