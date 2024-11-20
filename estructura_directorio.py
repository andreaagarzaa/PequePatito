# estructura_directorio.py

class TablaVariables:
    def __init__(self):
        # Diccionario que almacena variables por ámbito
        self.variables = {"global": {}}
        # Contadores para asignar direcciones de memoria según el tipo y ámbito
        self.contadores = {
            'global': {'entero': 1000, 'flotante': 2000},
            'local': {'entero': 3000, 'flotante': 4000},
            'temporal': {'entero': 5000, 'flotante': 6000}
        }

    def agregar_variable(self, nombre, tipo, ambito):
        if ambito not in self.variables:
            self.variables[ambito] = {}
        if nombre in self.variables[ambito]:
            return False  # La variable ya existe en el ámbito
        # Seleccionar el contador adecuado según el ámbito y tipo
        if ambito == 'global':
            direccion = self.contadores['global'][tipo]
            self.contadores['global'][tipo] += 1
        else:
            direccion = self.contadores['local'][tipo]
            self.contadores['local'][tipo] += 1
        # Agregar la variable con su tipo y dirección
        self.variables[ambito][nombre] = {'tipo': tipo, 'direccion': direccion}
        return True

    def obtener_variable(self, nombre, ambito):
        # Buscar la variable en el ámbito actual
        if nombre in self.variables.get(ambito, {}):
            return self.variables[ambito][nombre]
        # Si no se encuentra, buscar en el ámbito global
        if nombre in self.variables.get("global", {}):
            return self.variables["global"][nombre]
        return None  # Variable no encontrada

    def imprimir_tabla(self):
        print("==== Tablas de Variables ====\n")
        for ambito, vars in self.variables.items():
            print(f"{ambito.capitalize()}:")
            for var, attrs in vars.items():
                print(f"  - {var}: {attrs}")
            print()

class DirectorioFunciones:
    def __init__(self):
        # Diccionario que almacena funciones con sus atributos
        self.funciones = {"global": {"tipo_retorno": "nula", "parametros": [], "variables_locales": {}, "cuadruplo_inicio": None}}

    def agregar_funcion(self, nombre, tipo_retorno, parametros, variables_locales={}, cuadruplo_inicio=None):
        if nombre in self.funciones:
            return False  # La función ya existe
        self.funciones[nombre] = {
            "tipo_retorno": tipo_retorno,
            "parametros": parametros,
            "variables_locales": variables_locales,
            "cuadruplo_inicio": cuadruplo_inicio
        }
        return True

    def imprimir_directorio(self):
        print("==== Directorio de Funciones ====\n")
        for func, attrs in self.funciones.items():
            print(f"Función '{func}':")
            print(f"  Tipo de Retorno: {attrs['tipo_retorno']}")
            print(f"  Parámetros: {', '.join([f'{p['nombre']}:{p['tipo']}' for p in attrs['parametros']]) if attrs['parametros'] else 'Ninguno'}")
            print(f"  Tabla de Variables:")
            for var, attr in attrs['variables_locales'].items():
                print(f"    - {var}: {attr}")
            print(f"  Cuádruplo de Inicio: {attrs['cuadruplo_inicio']}\n")
