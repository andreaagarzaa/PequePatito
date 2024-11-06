# estructura_directorio.py

class TablaVariables:
    def __init__(self):
        # Diccionario con el ámbito como clave y otro diccionario de variables como valor
        self.variables = {"global": {}}

    def agregar_variable(self, nombre, tipo, ambito):
        if ambito not in self.variables:
            self.variables[ambito] = {}
        self.variables[ambito][nombre] = {'tipo': tipo}

    def obtener_tipo_variable(self, nombre, ambito):
        # Buscar en el ámbito actual
        if nombre in self.variables.get(ambito, {}):
            return self.variables[ambito][nombre]['tipo']
        # Buscar en el ámbito global si no se encuentra
        if nombre in self.variables.get("global", {}):
            return self.variables["global"][nombre]['tipo']
        return None

    def imprimir_tabla(self):
        print("==== Tablas de Variables ====\n")
        for ambito, vars in self.variables.items():
            print(f"{ambito.capitalize()}:")
            for var, attrs in vars.items():
                print(f"  - {var}: {attrs}")
            print()

class DirectorioFunciones:
    def __init__(self):
        # Diccionario de funciones con sus atributos
        self.funciones = {"global": {"tipo_retorno": "nula", "parametros": [], "variables_locales": {}, "cuadruplo_inicio": None}}

    def agregar_funcion(self, nombre, tipo_retorno, parametros):
        if nombre in self.funciones:
            return False  # Función ya existe
        self.funciones[nombre] = {
            "tipo_retorno": tipo_retorno,
            "parametros": parametros,
            "variables_locales": {},
            "cuadruplo_inicio": None
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
