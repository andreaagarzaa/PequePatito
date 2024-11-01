# peque_patito_listener.py
from antlr4 import ParseTreeListener


class PequePatitoListener(ParseTreeListener):
    def __init__(self, cubo_semantico, tabla_variables, directorio_funciones):
        self.cubo_semantico = cubo_semantico
        self.tabla_variables = tabla_variables
        self.directorio_funciones = directorio_funciones
        self.ambito_actual = "global"  # Ambito inicial
        self.pila_scopes = ["global"]  # Pila para manejar scopes
        self.errores = []  # Lista para almacenar errores semánticos

    def enterPrograma(self, ctx):
        print("Inicio del programa.")

    def exitPrograma(self, ctx):
        print("Fin del programa.")

    def enterVar_declaracion(self, ctx):
        """
        Procesa las declaraciones de variables en el ámbito actual y asegura que cada variable se registre.
        """
        scope_actual = self.pila_scopes[-1]  # Obtener el scope actual desde la pila
        variables = ctx.id_list().ID()  # Lista de variables declaradas en esta instrucción
        tipo = ctx.tipo().getText()  # Tipo de las variables

        for var in variables:
            nombre_var = var.getText()
            # Verificar si la variable ya ha sido declarada en el scope actual
            if nombre_var in self.tabla_variables.variables[scope_actual]:
                self.errores.append(
                    f"Error: Variable '{nombre_var}' ya declarada en el ámbito '{scope_actual}'.")
            else:
                # Agregar la variable a la tabla de variables actual
                self.tabla_variables.agregar_variable(nombre_var, tipo, scope_actual)
                # También agregarla al directorio de funciones si es global
                if scope_actual == "global":
                    self.directorio_funciones.funciones["global"]["variables_locales"][nombre_var] = {'tipo': tipo}
                else:
                    self.directorio_funciones.funciones[scope_actual]["variables_locales"][nombre_var] = {'tipo': tipo}
            print(f"Declaración de variable '{nombre_var}' de tipo '{tipo}' en ámbito '{scope_actual}'")

    def enterFuncs(self, ctx):
        """
        Procesa la declaración de funciones y cambia el ámbito actual a la función declarada.
        """
        tipo_funcion = "nula"
        func_id = ctx.ID().getText()

        # Validar duplicados en el directorio de funciones
        if self.directorio_funciones.obtener_funcion(func_id) is not None:
            print(f"Error: La función '{func_id}' ya ha sido declarada.")
        else:
            # Agregar función al directorio y cambiar el ámbito a la función actual
            self.directorio_funciones.agregar_funcion(func_id, tipo_funcion)
            self.ambito_actual = func_id
            self.pila_scopes.append(func_id)  # Cambiar al ámbito de la función
            print(f"Declaración de función '{func_id}' de tipo '{tipo_funcion}'")

            # Agregar parámetros de la función
            if ctx.params() is not None:
                for param in ctx.params().getText().split(','):
                    nombre_param, tipo_param = param.split(':')
                    nombre_param = nombre_param.strip()
                    tipo_param = tipo_param.strip()
                    # Agregar parámetro a la tabla de variables y directorio de funciones
                    self.tabla_variables.agregar_variable(nombre_param, tipo_param, func_id)
                    self.directorio_funciones.agregar_parametro(func_id, nombre_param, tipo_param)
                    print(f"  Parámetro '{nombre_param}' de tipo '{tipo_param}' en función '{func_id}'")

    def exitFuncs(self, ctx):
        # Regresar al ámbito global después de salir de la función
        self.pila_scopes.pop()
        self.ambito_actual = self.pila_scopes[-1]  # Restaurar el scope anterior


