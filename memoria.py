# memoria_ejecucion.py

class MemoriaEjecucion:
    def __init__(self):
        self.memoria = {}

    def escribir(self, direccion, valor):
        self.memoria[direccion] = valor

    def leer(self, direccion):
        return self.memoria.get(direccion, None)

    def imprimir_memoria(self):
        print("==== Memoria de Ejecución ====")
        for direccion, valor in sorted(self.memoria.items()):
            print(f"Dirección: {direccion}, Valor: {valor}")
