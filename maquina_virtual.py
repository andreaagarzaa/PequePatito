# maquina_virtual.py

class MaquinaVirtual:
    def __init__(self, cuadruplos, tabla_constantes, tabla_variables, directorio_funciones):
        """
        Inicializa la máquina virtual con las estructuras necesarias.
        """
        self.cuadruplos = cuadruplos
        self.tabla_constantes = tabla_constantes
        self.tabla_variables = tabla_variables
        self.directorio_funciones = directorio_funciones
        self.memoria_global = {}          # Memoria global
        self.memoria_constantes = {}      # Memoria para constantes
        self.pila_contextos = []          # Pila para manejar llamadas a funciones
        self.memoria_local_actual = {}    # Memoria local actual
        self.contador = 0                 # Contador de programa

        # Construir un mapeo de direcciones a tipos desde tabla_variables
        self.dir_a_tipo = {}
        for scope in self.tabla_variables.variables:
            variables_scope = self.tabla_variables.variables[scope]
            for var_name, var_info in variables_scope.items():
                direccion = var_info['direccion']
                tipo = var_info['tipo']
                self.dir_a_tipo[direccion] = tipo

        # Construir un mapeo de direcciones a tipos desde tabla_constantes
        for direccion, const_info in self.tabla_constantes.constantes_direccion.items():
            tipo = const_info['tipo']
            self.dir_a_tipo[direccion] = tipo
            self.memoria_constantes[direccion] = const_info['valor']

    def ejecutar(self):
        """
        Ejecuta los cuádruplos generados.
        """
        while self.contador < len(self.cuadruplos):
            cuadruplo = self.cuadruplos[self.contador]
            operador, op1, op2, res = cuadruplo
            print(f"\nEjecutando cuádruplo {self.contador}: {cuadruplo}")
            print(f"Contador antes de la operación: {self.contador}")

            # Variable para controlar si incrementamos el contador al final
            contador_incrementado = True

            if operador == 'GOTO':
                print(f"Saltando a cuádruplo {res}")
                self.contador = res
                contador_incrementado = False

            elif operador == 'GOTOF':
                valor = self.obtener_valor(op1)
                print(f"Evaluando GOTOF: {valor}")
                if not valor:
                    print(f"Condición falsa, saltando a cuádruplo {res}")
                    self.contador = res
                    contador_incrementado = False
                else:
                    print(f"Condición verdadera, continuando ejecución")

            elif operador == '=':
                valor = self.obtener_valor(op1)
                self.asignar_valor(res, valor)
                print(f"Asignación: dirección {res} = {valor}")

            elif operador in ['+', '-', '*', '/']:
                val1 = self.obtener_valor(op1)
                val2 = self.obtener_valor(op2)
                print(f"Operación: {val1} {operador} {val2}")
                resultado = self.realizar_operacion(operador, val1, val2)
                if resultado is not None:
                    self.asignar_valor(res, resultado)
                    print(f"Resultado almacenado en dirección {res}: {resultado}")
                else:
                    print(f"Operación fallida: {operador}")

            elif operador in ['>', '<', '>=', '<=', '==', '!=']:
                val1 = self.obtener_valor(op1)
                val2 = self.obtener_valor(op2)
                print(f"Comparación: {val1} {operador} {val2}")
                resultado = self.realizar_operacion_relacional(operador, val1, val2)
                if resultado is not None:
                    self.asignar_valor(res, resultado)
                    print(f"Resultado almacenado en dirección {res}: {resultado}")
                else:
                    print(f"Comparación fallida: {operador}")

            elif operador == 'print':
                valor = self.obtener_valor(op1)
                print(f"Salida: {valor}")

            elif operador == 'ERA':
                # Preparar activación para la función
                self.preparar_activacion(op1)

            elif operador == 'PARAM':
                # Asignar valor al parámetro de la función
                self.asignar_parametro(op1, res)

            elif operador == 'GOSUB':
                # Llamar a la función
                self.llamar_funcion(op1, res)
                contador_incrementado = False

            elif operador == 'ENDPROC':
                # Terminar ejecución de función
                self.terminar_funcion()
                contador_incrementado = False

            elif operador == 'END':
                print("Fin de la ejecución.")
                break

            else:
                print(f"Operador no reconocido: {operador}")

            # Incrementar el contador si no se ha modificado en la operación
            if contador_incrementado:
                self.contador += 1

            print(f"Contador después de la operación: {self.contador}")
            print(f"Estado de la memoria global: {self.memoria_global}")
            print(f"Estado de la memoria local actual: {self.memoria_local_actual}")

    def obtener_valor(self, direccion):
        """
        Obtiene el valor de una dirección de memoria.
        """
        if direccion in self.memoria_local_actual:
            return self.memoria_local_actual[direccion]
        elif direccion in self.memoria_global:
            return self.memoria_global[direccion]
        elif direccion in self.memoria_constantes:
            return self.memoria_constantes[direccion]
        else:
            print(f"Advertencia: Dirección {direccion} no inicializada.")
            return None

    def asignar_valor(self, direccion, valor):
        """
        Asigna un valor a una dirección de memoria, respetando el tipo.
        """
        tipo = self.dir_a_tipo.get(direccion)
        if tipo:
            # Convertir valor al tipo correcto
            try:
                if tipo == 'entero':
                    valor = int(valor)
                elif tipo == 'flotante':
                    valor = float(valor)
                elif tipo == 'booleano':
                    valor = bool(valor)
                elif tipo == 'cadena':
                    valor = str(valor)
            except ValueError as ve:
                print(f"Error de conversión: No se puede convertir {valor} a {tipo}.")
                return

        if self.es_direccion_local(direccion):
            self.memoria_local_actual[direccion] = valor
            print(f"Asignado valor {valor} a dirección local {direccion}")
        else:
            self.memoria_global[direccion] = valor
            print(f"Asignado valor {valor} a dirección global {direccion}")

    def es_direccion_local(self, direccion):
        """
        Verifica si una dirección pertenece al ámbito local.
        """
        # Direcciones locales: 4000-6999
        return 4000 <= direccion < 7000

    def realizar_operacion(self, operador, val1, val2):
        """
        Realiza una operación aritmética.
        """
        try:
            if operador == '+':
                return val1 + val2
            elif operador == '-':
                return val1 - val2
            elif operador == '*':
                return val1 * val2
            elif operador == '/':
                if val2 == 0:
                    raise ZeroDivisionError("Error: División entre cero.")
                return val1 / val2
        except Exception as e:
            print(f"Error realizando operación {val1} {operador} {val2}: {e}")
            return None

    def realizar_operacion_relacional(self, operador, val1, val2):
        """
        Realiza una operación relacional.
        """
        try:
            if operador == '>':
                return val1 > val2
            elif operador == '<':
                return val1 < val2
            elif operador == '>=':
                return val1 >= val2
            elif operador == '<=':
                return val1 <= val2
            elif operador == '==':
                return val1 == val2
            elif operador == '!=':
                return val1 != val2
        except Exception as e:
            print(f"Error realizando comparación {val1} {operador} {val2}: {e}")
            return None

    def preparar_activacion(self, nombre_funcion):
        """
        Prepara la activación para una función, almacenando el contexto actual.
        """
        print(f"Preparando activación para la función '{nombre_funcion}'")
        # Crear un nuevo contexto para la función sin establecer return_address aquí
        self.pila_contextos.append({
            'nombre_funcion': nombre_funcion,
            'memoria_local': self.memoria_local_actual.copy()
            # 'return_address' se establecerá en llamar_funcion
        })
        self.memoria_local_actual = {}

    def asignar_parametro(self, valor_direccion, parametro):
        """
        Asigna un parámetro a una función.
        """
        valor = self.obtener_valor(valor_direccion)
        param_num = int(parametro.replace('param', '')) - 1
        nombre_funcion = self.obtener_nombre_funcion_actual()
        funcion_info = self.directorio_funciones.funciones.get(nombre_funcion, None)

        if funcion_info and param_num < len(funcion_info['parametros']):
            param_name = funcion_info['parametros'][param_num]['nombre']
            param_direccion = self.tabla_variables.obtener_variable(param_name, nombre_funcion)['direccion']
            self.memoria_local_actual[param_direccion] = valor
            print(f"Asignando valor {valor} al parámetro '{param_name}' en dirección {param_direccion}")
        else:
            print(f"Error: Parámetro {param_num + 1} fuera de rango para la función '{nombre_funcion}'")

    def llamar_funcion(self, nombre_funcion, cuadruplo_inicio):
        """
        Llama a una función, almacenando el return_address y saltando al inicio de la función.
        """
        print(f"Llamando a la función '{nombre_funcion}' en cuádruplo {cuadruplo_inicio}")
        if self.pila_contextos:
            contexto_actual = self.pila_contextos[-1]
            contexto_actual['return_address'] = self.contador + 1
            print(f"Guardando return_address {self.contador + 1} en el contexto")
        else:
            print("Error: No hay contexto actual para guardar return_address")
        self.contador = cuadruplo_inicio
        print(f"Contador actualizado para llamada a función: {self.contador}")

    def terminar_funcion(self):
        """
        Termina la ejecución de una función, restaurando el contexto anterior.
        """
        if not self.pila_contextos:
            print("Error: No hay contexto para terminar la función.")
            self.contador = len(self.cuadruplos)  # Terminar ejecución
            return

        contexto = self.pila_contextos.pop()
        self.memoria_local_actual = contexto['memoria_local']
        return_address = contexto.get('return_address', None)

        if return_address is not None:
            print(f"Regresando al contexto anterior. Contador de retorno: {return_address}")
            self.contador = return_address
        else:
            print("Error: No se encontró return_address en el contexto.")
            self.contador = len(self.cuadruplos)  # Terminar ejecución

    def obtener_nombre_funcion_actual(self):
        """
        Obtiene el nombre de la función actual desde la pila de contextos.
        """
        if self.pila_contextos:
            return self.pila_contextos[-1].get('nombre_funcion', 'global')
        else:
            return 'global'
