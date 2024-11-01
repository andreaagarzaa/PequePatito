# estructura_directorio.py

class TablaVariables:
    def __init__(self):
        self.variables = {"global": {}}

    def agregar_variable(self, nombre, tipo, scope="global"):
        if scope not in self.variables:
            self.variables[scope] = {}
        if nombre in self.variables[scope]:
            raise Exception(f"Variable '{nombre}' ya declarada en el ámbito '{scope}'.")
        self.variables[scope][nombre] = {'tipo': tipo}

    def obtener_tipo_variable(self, nombre, scope="global"):
        return self.variables.get(scope, {}).get(nombre, {}).get('tipo', None)

    def imprimir_tabla(self):
        print("==== Tablas de Variables ====")
        for scope, vars_dict in self.variables.items():
            print(f"\n{scope.capitalize()}:")
            for nombre, detalles in vars_dict.items():
                print(f"  - {nombre}: {detalles}")

class DirectorioFunciones:
    def __init__(self):
        self.funciones = {"global": {"tipo": "nula", "parametros": {}, "variables_locales": {}}}

    def agregar_funcion(self, func_id, tipo_funcion):
        if func_id in self.funciones:
            raise Exception(f"Función '{func_id}' ya declarada.")
        self.funciones[func_id] = {
            "tipo": tipo_funcion,
            "parametros": {},
            "variables_locales": {}
        }

    def obtener_funcion(self, func_id):
        return self.funciones.get(func_id, None)

    def agregar_parametro(self, func_id, nombre_param, tipo_param):
        if func_id not in self.funciones:
            raise Exception(f"La función '{func_id}' no está declarada.")
        self.funciones[func_id]["parametros"][nombre_param] = tipo_param

    def agregar_variable_local(self, func_id, nombre_var, tipo_var):
        if func_id not in self.funciones:
            raise Exception(f"La función '{func_id}' no está declarada.")
        if nombre_var in self.funciones[func_id]["variables_locales"]:
            raise Exception(f"Variable '{nombre_var}' ya declarada en la función '{func_id}'.")
        self.funciones[func_id]["variables_locales"][nombre_var] = {'tipo': tipo_var}

    def imprimir_directorio(self):
        print("\n==== Directorio de Funciones ====")
        for func_id, detalles in self.funciones.items():
            print(f"\nFunción '{func_id}':")
            print(f"  Tipo de Retorno: {detalles['tipo']}")
            if detalles["parametros"]:
                print("  Parámetros:")
                for nombre, tipo in detalles['parametros'].items():
                    print(f"    - {nombre}: {tipo}")
            else:
                print("  Parámetros: Ninguno")
            if detalles["variables_locales"]:
                print("  Tabla de Variables:")
                for nombre, var_detalles in detalles['variables_locales'].items():
                    print(f"    - {nombre}: {var_detalles}")
            else:
                print("  Tabla de Variables: Ninguno")
            print("  Cuádruplo de Inicio: None")
