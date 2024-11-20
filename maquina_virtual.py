# maquina_virtual.py

class MaquinaVirtual:
    def __init__(self, cuadruplos, tabla_constantes, tabla_variables):
        self.cuadruplos = cuadruplos
        self.tabla_constantes = tabla_constantes
        self.tabla_variables = tabla_variables
        self.memoria = {}  # Memoria de ejecución
        self.pila_llamadas = []
        self.contador = 0  # Contador de programa

        # Construir un mapeo de direcciones a tipos
        self.dir_a_tipo = {}

        # Desde tabla_variables
        for scope in self.tabla_variables.variables:
            variables_scope = self.tabla_variables.variables[scope]
            for var_name, var_info in variables_scope.items():
                direccion = var_info['direccion']
                tipo = var_info['tipo']
                self.dir_a_tipo[direccion] = tipo

        # Desde tabla_constantes
        for direccion, const_info in self.tabla_constantes.constantes_direccion.items():
            tipo = const_info['tipo']
            self.dir_a_tipo[direccion] = tipo

    def ejecutar(self):
        contador = self.contador
        while contador < len(self.cuadruplos):
            cuadruplo = self.cuadruplos[contador]
            operador, op1, op2, res = cuadruplo
            print(f"\nEjecutando cuádruplo {contador}: {cuadruplo}")

            if operador == 'GOTO':
                print(f"Saltando a cuádruplo {res}")
                contador = res - 1
            elif operador == 'GOTOF':
                valor = self.obtener_valor(op1)
                print(f"Evaluando GOTOF: {valor}")
                if not valor:
                    print(f"Condición falsa, saltando a cuádruplo {res}")
                    contador = res - 1
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
                self.asignar_valor(res, resultado)
                print(f"Resultado almacenado en dirección {res}: {resultado}")
            elif operador in ['>', '<', '>=', '<=', '==', '!=']:
                val1 = self.obtener_valor(op1)
                val2 = self.obtener_valor(op2)
                print(f"Comparación: {val1} {operador} {val2}")
                resultado = self.realizar_operacion_relacional(operador, val1, val2)
                self.asignar_valor(res, resultado)
                print(f"Resultado almacenado en dirección {res}: {resultado}")
            elif operador == 'print':
                valor = self.obtener_valor(op1)
                print(f"Salida: {valor}")
            elif operador == 'END':
                print("Fin de la ejecución.")
                break
            else:
                print(f"Operador no reconocido: {operador}")
            print(f"Estado de la memoria: {self.memoria}")
            contador += 1

    def obtener_valor(self, direccion):
        if direccion in self.memoria:
            return self.memoria[direccion]
        elif direccion in self.tabla_constantes.constantes_direccion:
            constante = self.tabla_constantes.constantes_direccion[direccion]
            return constante['valor']
        else:
            # Puede ser una dirección de variable no inicializada
            print(f"Advertencia: Dirección {direccion} no inicializada.")
            return None

    def asignar_valor(self, direccion, valor):
        tipo = self.dir_a_tipo.get(direccion)
        if tipo:
            # Convertir valor al tipo correcto
            if tipo == 'entero':
                valor = int(valor)
            elif tipo == 'flotante':
                valor = float(valor)
            elif tipo == 'booleano':
                valor = bool(valor)
            elif tipo == 'cadena':
                valor = str(valor)
        else:
            # Tipo desconocido, no convertimos
            pass

        self.memoria[direccion] = valor
        print(f"Asignado valor {valor} a dirección {direccion}")

    def realizar_operacion(self, operador, val1, val2):
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

    def realizar_operacion_relacional(self, operador, val1, val2):
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
