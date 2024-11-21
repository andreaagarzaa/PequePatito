# peque_patito_listener.py

from antlr4 import ParseTreeListener
from pilas_cuadruplos import PilasCuadruplos
from fila_cuadruplos import FilaCuadruplos
from gen.PequePatitoParser import PequePatitoParser
from tabla_constantes import TablaConstantes

class PequePatitoListener(ParseTreeListener):
    def __init__(self, cubo_semantico, tabla_variables, directorio_funciones):
        self.cubo_semantico = cubo_semantico
        self.tabla_variables = tabla_variables
        self.tabla_variables_actual = self.tabla_variables.variables
        self.directorio_funciones = directorio_funciones
        self.ambito_actual = "global"
        self.pila_scopes = ["global"]
        self.errores = []
        self.lista_param_impresion = []
        self.pila_parametros = []
        self.pilas = PilasCuadruplos()
        self.fila_cuadruplos = FilaCuadruplos()
        self.cont_temp = 0
        self.tabla_constantes = TablaConstantes()
        self.fila_cuadruplos.agregar_cuadruplo('GOTO', None, None, None)
        self.memoria_ejecucion = {}
        self.funcion_actual = None
        self.param_contador = 0

    def generar_temporal(self, tipo):
        direccion = self.tabla_variables.contadores['temporal'][tipo]
        temp = f"t{self.cont_temp}"
        self.cont_temp += 1
        self.tabla_variables.contadores['temporal'][tipo] += 1
        self.tabla_variables.variables.setdefault('temporal', {})[temp] = {'tipo': tipo, 'direccion': direccion}
        return direccion

    def exitPrograma(self, ctx: PequePatitoParser.ProgramaContext):
        self.fila_cuadruplos.agregar_cuadruplo('END', None, None, None)

    def enterInicio(self, ctx: PequePatitoParser.InicioContext):
        if self.ambito_actual == 'global' and not hasattr(self, 'main_goto_updated'):
            # Actualizar el cuádruplo GOTO inicial con la dirección actual
            self.fila_cuadruplos.cuadruplos[0] = (
                'GOTO',
                None,
                None,
                len(self.fila_cuadruplos.cuadruplos)
            )
            self.main_goto_updated = True

    # Métodos para manejar declaraciones de variables
    def enterVar_declaracion(self, ctx: PequePatitoParser.Var_declaracionContext):
        scope_actual = self.pila_scopes[-1]
        variables = ctx.id_list().ID()
        tipo = ctx.tipo().getText()

        for var in variables:
            nombre_var = var.getText()
            if not self.tabla_variables.agregar_variable(nombre_var, tipo, scope_actual):
                self.errores.append(
                    f"Error: Variable '{nombre_var}' ya declarada en el ámbito '{scope_actual}'.")
            else:
                variable_info = self.tabla_variables.obtener_variable(nombre_var, scope_actual)
                direccion = variable_info['direccion']
                print(
                    f"Declaración de variable '{nombre_var}' de tipo '{tipo}' en ámbito '{scope_actual}' con dirección '{direccion}'")
                # Agregar la variable a las variables locales de la función en el directorio de funciones
                if scope_actual != 'global':
                    self.directorio_funciones.funciones[scope_actual]['variables_locales'][nombre_var] = {
                        'tipo': tipo,
                        'direccion': direccion
                    }

    def enterFuncs(self, ctx: PequePatitoParser.FuncsContext):
        nombre_funcion = ctx.ID().getText()
        tipo_retorno = ctx.getChild(0).getText()

        if nombre_funcion in self.directorio_funciones.funciones:
            self.errores.append(f"Error: Función '{nombre_funcion}' ya declarada.")
        else:
            parametros = []
            variables_locales = {}
            if ctx.params():
                params_list = ctx.params().getText().split(',')
                for param in params_list:
                    if ':' in param:
                        param_nombre, param_tipo = param.split(':')
                        parametros.append({'nombre': param_nombre, 'tipo': param_tipo})
                    else:
                        self.errores.append(f"Error: Error en declaración de parámetros de función '{nombre_funcion}'.")

            # Agregar la función al directorio
            self.directorio_funciones.agregar_funcion(
                nombre_funcion,
                tipo_retorno,
                parametros,
                variables_locales,  # Variables locales incluyen parámetros
                len(self.fila_cuadruplos.cuadruplos)
            )
            # Generar cuádruplo de inicio de función
            self.fila_cuadruplos.agregar_cuadruplo('FUNC', nombre_funcion, None, None)
            self.ambito_actual = nombre_funcion
            self.pila_scopes.append(nombre_funcion)
            print(f"Entrando a la función '{nombre_funcion}' con tipo de retorno '{tipo_retorno}'")

            # Agregar parámetros a la tabla de variables
            for param in parametros:
                param_nombre = param['nombre']
                param_tipo = param['tipo']
                if not self.tabla_variables.agregar_variable(param_nombre, param_tipo, nombre_funcion):
                    self.errores.append(
                        f"Error: Parámetro '{param_nombre}' ya declarado en la función '{nombre_funcion}'.")
                else:
                    variable_info = self.tabla_variables.obtener_variable(param_nombre, nombre_funcion)
                    direccion = variable_info['direccion']
                    # Agregar parámetro a las variables locales de la función
                    variables_locales[param_nombre] = {'tipo': param_tipo, 'direccion': direccion}

    def exitFuncs(self, ctx: PequePatitoParser.FuncsContext):
        self.fila_cuadruplos.agregar_cuadruplo('ENDPROC', None, None, None)
        self.pila_scopes.pop()
        self.ambito_actual = self.pila_scopes[-1]

    def enterFactor(self, ctx: PequePatitoParser.FactorContext):
        if ctx.ID():
            nombre_var = ctx.ID().getText()
            scope_actual = self.pila_scopes[-1]
            variable_info = self.tabla_variables.obtener_variable(nombre_var, scope_actual)
            if not variable_info:
                variable_info = self.tabla_variables.obtener_variable(nombre_var, "global")
                if not variable_info:
                    self.errores.append(f"Error: Variable '{nombre_var}' no declarada en el ámbito '{scope_actual}'.")

    def exitFactor(self, ctx: PequePatitoParser.FactorContext):
        if ctx.NUMERO():
            valor = ctx.NUMERO().getText()
            if '.' in valor:
                tipo = 'flotante'
            else:
                tipo = 'entero'
            direccion = self.tabla_constantes.agregar_constante(valor, tipo)
            self.pilas.push_operando(direccion)
            self.pilas.push_tipo(tipo)
        elif ctx.ID():
            nombre_var = ctx.ID().getText()
            variable_info = self.tabla_variables.obtener_variable(nombre_var, self.ambito_actual)
            if not variable_info:
                variable_info = self.tabla_variables.obtener_variable(nombre_var, "global")
            if variable_info:
                direccion = variable_info['direccion']
                tipo = variable_info['tipo']
                self.pilas.push_operando(direccion)
                self.pilas.push_tipo(tipo)
            else:
                self.errores.append(f"Error: Variable '{nombre_var}' no declarada en el ámbito '{self.ambito_actual}'.")
        elif ctx.expresion():
            pass
        else:
            # Agregar manejo para VERDADERO y FALSO (si aplica)
            # if ctx.VERDADERO() or ctx.FALSO():
            #     valor = ctx.getText()
            #     tipo = 'booleano'
            #     direccion = self.tabla_constantes.agregar_constante(valor, tipo)
            #     self.pilas.push_operando(direccion)
            #     self.pilas.push_tipo(tipo)

          pass

    def enterOperador(self, ctx: PequePatitoParser.OperadorContext):
        operador = ctx.getText()
        self.pilas.push_operador(operador)

    def enterOperador_factor(self, ctx: PequePatitoParser.Operador_factorContext):
        operador = ctx.getText()
        self.pilas.push_operador(operador)

    def enterBo(self, ctx: PequePatitoParser.BoContext):
        operador = ctx.getText()
        self.pilas.push_operador(operador)

    def exitTermino(self, ctx: PequePatitoParser.TerminoContext):
        while self.pilas.pila_operadores and self.pilas.pila_operadores[-1] in ['*', '/']:
            operador = self.pilas.pop_operador()
            operando_derecho = self.pilas.pop_operando()
            tipo_derecho = self.pilas.pop_tipo()
            operando_izquierdo = self.pilas.pop_operando()
            tipo_izquierdo = self.pilas.pop_tipo()
            print(f"Operación: {operando_izquierdo} {operador} {operando_derecho}")
            print(f"Tipos: {tipo_izquierdo}, {tipo_derecho}")
            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo_izquierdo, tipo_derecho, operador)
            if tipo_resultado == 'error':
                self.errores.append(
                    f"Error de tipos: No se puede aplicar operador '{operador}' a tipos '{tipo_izquierdo}' y '{tipo_derecho}'.")
            else:
                temp_direccion = self.generar_temporal(tipo_resultado)
                self.fila_cuadruplos.agregar_cuadruplo(operador, operando_izquierdo, operando_derecho, temp_direccion)
                self.pilas.push_operando(temp_direccion)
                self.pilas.push_tipo(tipo_resultado)

    def exitExp(self, ctx: PequePatitoParser.ExpContext):
        while self.pilas.pila_operadores and self.pilas.pila_operadores[-1] in ['+', '-']:
            operador = self.pilas.pop_operador()
            operando_derecho = self.pilas.pop_operando()
            tipo_derecho = self.pilas.pop_tipo()
            operando_izquierdo = self.pilas.pop_operando()
            tipo_izquierdo = self.pilas.pop_tipo()
            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo_izquierdo, tipo_derecho, operador)
            if tipo_resultado == 'error':
                self.errores.append(
                    f"Error de tipos: No se puede aplicar operador '{operador}' a tipos '{tipo_izquierdo}' y '{tipo_derecho}'.")
            else:
                temp_direccion = self.generar_temporal(tipo_resultado)
                self.pilas.push_operando(temp_direccion)
                self.pilas.push_tipo(tipo_resultado)
                self.fila_cuadruplos.agregar_cuadruplo(operador, operando_izquierdo, operando_derecho, temp_direccion)

    def exitExpresion(self, ctx: PequePatitoParser.ExpresionContext):
        if ctx.bo():
            operador = self.pilas.pop_operador()
            operando_derecho = self.pilas.pop_operando()
            tipo_derecho = self.pilas.pop_tipo()
            operando_izquierdo = self.pilas.pop_operando()
            tipo_izquierdo = self.pilas.pop_tipo()
            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo_izquierdo, tipo_derecho, operador)
            if tipo_resultado == 'error':
                self.errores.append(
                    f"Error de tipos: No se puede aplicar operador relacional '{operador}' a tipos '{tipo_izquierdo}' y '{tipo_derecho}'.")
            else:
                temp_direccion = self.generar_temporal(tipo_resultado)
                self.pilas.push_operando(temp_direccion)
                self.pilas.push_tipo(tipo_resultado)
                self.fila_cuadruplos.agregar_cuadruplo(operador, operando_izquierdo, operando_derecho, temp_direccion)
                print(f"Operando izquierdo: {operando_izquierdo}, Tipo: {tipo_izquierdo}")
                print(f"Operando derecho: {operando_derecho}, Tipo: {tipo_derecho}")

        if self.es_expresion_de_condicion(ctx):
            print("Detectada expresión de condición en exitExpresion")
            resultado = self.pilas.pop_operando()
            tipo = self.pilas.pop_tipo()
            if tipo != 'booleano':
                self.errores.append(f"Error: La condición debe ser de tipo booleano, pero es '{tipo}'.")
            else:
                self.fila_cuadruplos.agregar_cuadruplo('GOTOF', resultado, None, None)
                self.pilas.push_salto(len(self.fila_cuadruplos.cuadruplos) - 1)
                print(f"Se generó cuádruplo GOTOF en condición, índice: {len(self.fila_cuadruplos.cuadruplos) - 1}")
        elif self.es_expresion_de_ciclo(ctx):
            print("Detectada expresión de ciclo en exitExpresion")
            resultado = self.pilas.pop_operando()
            tipo = self.pilas.pop_tipo()
            if tipo != 'booleano':
                self.errores.append(f"Error: La condición del ciclo debe ser de tipo booleano, pero es '{tipo}'.")
            else:
                self.fila_cuadruplos.agregar_cuadruplo('GOTOF', resultado, None, None)
                self.pilas.push_salto(len(self.fila_cuadruplos.cuadruplos) - 1)
                print(f"Se generó cuádruplo GOTOF en ciclo, índice: {len(self.fila_cuadruplos.cuadruplos) - 1}")
        elif self.is_in_function_call():
            # Manejo de parámetros en llamada a función
            param_value = self.pilas.pop_operando()
            param_type = self.pilas.pop_tipo()
            nombre_funcion = self.funcion_actual
            funcion_info = self.directorio_funciones.funciones[nombre_funcion]
            if self.param_contador >= len(funcion_info['parametros']):
                self.errores.append(f"Error: La función '{nombre_funcion}' no esperaba más parámetros.")
                return
            expected_param = funcion_info['parametros'][self.param_contador]
            expected_type = expected_param['tipo']
            if param_type != expected_type:
                self.errores.append(f"Error: El parámetro {self.param_contador+1} de la función '{nombre_funcion}' esperaba un '{expected_type}', pero se recibió un '{param_type}'.")
            # Generar cuádruplo PARAM
            self.fila_cuadruplos.agregar_cuadruplo('PARAM', param_value, None, f"param{self.param_contador+1}")
            self.param_contador += 1

    # Métodos para manejar asignaciones
    def exitAsigna(self, ctx: PequePatitoParser.AsignaContext):
        variable = ctx.ID().getText()
        print(f"Asignando a variable '{variable}'")
        print(f"Pila de operandos antes de pop: {self.pilas.pila_operandos}")
        print(f"Pila de tipos antes de pop: {self.pilas.pila_tipos}")
        valor = self.pilas.pop_operando()
        tipo_valor = self.pilas.pop_tipo()
        if valor is None or tipo_valor is None:
            self.errores.append(f"Error: Valor o tipo no válido al asignar a la variable '{variable}'.")
            return
        variable_info = self.tabla_variables.obtener_variable(variable, self.ambito_actual)
        if not variable_info:
            variable_info = self.tabla_variables.obtener_variable(variable, "global")
        if variable_info is None:
            self.errores.append(f"Error: Variable '{variable}' no declarada.")
        else:
            tipo_variable = variable_info['tipo']
            direccion_variable = variable_info['direccion']
            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo_variable, tipo_valor, '=')
            if tipo_resultado == 'error':
                self.errores.append(
                    f"Error de tipos: No se puede asignar tipo '{tipo_valor}' a variable '{variable}' de tipo '{tipo_variable}'.")
            else:
                self.fila_cuadruplos.agregar_cuadruplo('=', valor, None, direccion_variable)

    # Métodos para manejar sentencias de impresión
    def enterImprime(self, ctx: PequePatitoParser.ImprimeContext):
        self.lista_param_impresion = []

    def exitImprime(self, ctx: PequePatitoParser.ImprimeContext):
        for parametro in self.lista_param_impresion:
            self.fila_cuadruplos.agregar_cuadruplo('print', parametro, None, None)
        self.lista_param_impresion = []

    def exitP_imp(self, ctx: PequePatitoParser.P_impContext):
        if ctx.expresion():
            expr_result = self.pilas.pop_operando()
            self.lista_param_impresion.insert(0, expr_result)
        elif ctx.LETRERO():
            cadena = ctx.LETRERO()[0].getText()
            direccion = self.tabla_constantes.agregar_constante(cadena, 'cadena')
            self.lista_param_impresion.insert(0, direccion)

    # Métodos para manejar sentencias condicionales
    def enterCondicion(self, ctx: PequePatitoParser.CondicionContext):
        pass  # Nada que hacer al entrar a la condición

    def exitCondicion(self, ctx: PequePatitoParser.CondicionContext):
        print(f"Llamando a exitCondicion. Pila de saltos antes de pop: {self.pilas.pila_saltos}")
        if ctx.else_part():
            # Si hay una parte else, los pops ya se manejaron
            pass
        else:
            # No hay else_part, realizamos el pop de la pila de saltos
            if not self.pilas.pila_saltos:
                self.errores.append("Error: Pila de saltos está vacía antes de hacer pop en exitCondicion.")
                return
            end = self.pilas.pop_salto()
            # Actualizar el cuádruplo GOTOF con la dirección correcta
            self.fila_cuadruplos.cuadruplos[end] = (
                self.fila_cuadruplos.cuadruplos[end][0],
                self.fila_cuadruplos.cuadruplos[end][1],
                self.fila_cuadruplos.cuadruplos[end][2],
                len(self.fila_cuadruplos.cuadruplos)
            )

    def enterElse_part(self, ctx: PequePatitoParser.Else_partContext):
        # Generar GOTO y hacer push a pila_saltos
        self.fila_cuadruplos.agregar_cuadruplo('GOTO', None, None, None)
        goto_indice = len(self.fila_cuadruplos.cuadruplos) - 1
        self.pilas.push_salto(goto_indice)
        # Pop del índice del GOTOF y actualizarlo al inicio del else
        if not self.pilas.pila_saltos:
            self.errores.append("Error: Pila de saltos está vacía antes de hacer pop en enterElse_part.")
            return
        falso = self.pilas.pop_salto()
        self.fila_cuadruplos.cuadruplos[falso] = (
            self.fila_cuadruplos.cuadruplos[falso][0],
            self.fila_cuadruplos.cuadruplos[falso][1],
            self.fila_cuadruplos.cuadruplos[falso][2],
            len(self.fila_cuadruplos.cuadruplos)
        )

    def exitElse_part(self, ctx: PequePatitoParser.Else_partContext):
        # Pop del índice del GOTO y actualizarlo al final del else
        if not self.pilas.pila_saltos:
            self.errores.append("Error: Pila de saltos está vacía antes de hacer pop en exitElse_part.")
            return
        end = self.pilas.pop_salto()
        self.fila_cuadruplos.cuadruplos[end] = (
            self.fila_cuadruplos.cuadruplos[end][0],
            self.fila_cuadruplos.cuadruplos[end][1],
            self.fila_cuadruplos.cuadruplos[end][2],
            len(self.fila_cuadruplos.cuadruplos)
        )

    # Métodos para manejar ciclos
    def enterCiclo(self, ctx: PequePatitoParser.CicloContext):
        # Push del inicio del ciclo
        self.pilas.push_salto(len(self.fila_cuadruplos.cuadruplos))

    def exitCiclo(self, ctx: PequePatitoParser.CicloContext):
        falso = self.pilas.pop_salto()
        retorno = self.pilas.pop_salto()
        self.fila_cuadruplos.agregar_cuadruplo('GOTO', None, None, retorno)
        # Actualizar el cuádruplo GOTOF con la dirección después del ciclo
        self.fila_cuadruplos.cuadruplos[falso] = (
            self.fila_cuadruplos.cuadruplos[falso][0],
            self.fila_cuadruplos.cuadruplos[falso][1],
            self.fila_cuadruplos.cuadruplos[falso][2],
            len(self.fila_cuadruplos.cuadruplos)
        )

    # Funciones para identificar expresiones de condición y ciclo
    def es_expresion_de_condicion(self, ctx):
        parent_ctx = ctx.parentCtx
        if isinstance(parent_ctx, PequePatitoParser.CondicionContext):
            # Verificar si la expresión es la condición del 'si'
            return parent_ctx.expresion() == ctx
        return False

    def es_expresion_de_ciclo(self, ctx):
        parent_ctx = ctx.parentCtx
        if isinstance(parent_ctx, PequePatitoParser.CicloContext):
            # Verificar si la expresión es la condición del 'mientras'
            return parent_ctx.expresion() == ctx
        return False

    # Métodos para manejar llamadas a funciones
    def enterLlamada(self, ctx: PequePatitoParser.LlamadaContext):
        nombre_funcion = ctx.ID().getText()
        if nombre_funcion not in self.directorio_funciones.funciones:
            self.errores.append(f"Error: La función '{nombre_funcion}' no está definida.")
            return
        # Start parameter counting
        self.funcion_actual = nombre_funcion
        self.param_contador = 0
        # Generate ERA quadruple
        self.fila_cuadruplos.agregar_cuadruplo('ERA', nombre_funcion, None, None)

    def exitLlamada(self, ctx: PequePatitoParser.LlamadaContext):
        nombre_funcion = ctx.ID().getText()
        funcion_info = self.directorio_funciones.funciones[nombre_funcion]
        num_params = len(funcion_info['parametros'])
        if self.param_contador != num_params:
            self.errores.append(f"Error: La función '{nombre_funcion}' esperaba {num_params} parámetros, pero se proporcionaron {self.param_contador}.")
        # Generate GOSUB quadruple
        cuadruplo_inicio = funcion_info['cuadruplo_inicio']
        self.fila_cuadruplos.agregar_cuadruplo('GOSUB', nombre_funcion, None, cuadruplo_inicio)
        # Si la función tiene tipo de retorno distinto de 'nula', manejar el valor de retorno
        tipo_retorno = funcion_info['tipo_retorno']
        if tipo_retorno != 'nula':
            temp_direccion = self.generar_temporal(tipo_retorno)
            self.direccion_funcion_llamada = temp_direccion
            self.tipo_funcion_llamada = tipo_retorno
            # No se genera cuádruplo para asignar valor de retorno ya que no manejamos retornos
        else:
            # Si la función no retorna valor, limpiar variables temporales
            self.direccion_funcion_llamada = None
            self.tipo_funcion_llamada = None
        # Reset function call tracking
        self.funcion_actual = None
        self.param_contador = 0

    def is_in_function_call(self):
        return self.funcion_actual is not None
