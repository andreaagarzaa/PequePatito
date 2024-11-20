# tabla_constantes.py
class TablaConstantes:
    def __init__(self):
        self.constantes = {}  # {valor: direccion}
        self.constantes_direccion = {}  # {direccion: {'valor': valor, 'tipo': tipo}}
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
            # Convertir valor al tipo correcto
            if tipo == 'entero':
                valor_converted = int(valor)
            elif tipo == 'flotante':
                valor_converted = float(valor)
            elif tipo == 'cadena':
                valor_converted = str(valor).strip('"')
            elif tipo == 'booleano':
                valor_converted = True if valor.lower() == 'verdadero' else False
            else:
                valor_converted = valor
            self.constantes_direccion[direccion] = {'valor': valor_converted, 'tipo': tipo}
            self.contadores[tipo] += 1
        return self.constantes[valor]

    def obtener_constante(self, direccion):
        return self.constantes_direccion.get(direccion, None)

    def imprimir_constantes(self):
        print("==== Tabla de Constantes ====")
        for valor, direccion in self.constantes.items():
            print(f"Valor: {valor}, Dirección: {direccion}")
        print("=============================")
