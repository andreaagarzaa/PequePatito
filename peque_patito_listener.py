# peque_patito_listener.py

from antlr4 import ParseTreeListener, TerminalNode
from pilas_cuadruplos import PilasCuadruplos
from fila_cuadruplos import FilaCuadruplos
from gen.PequePatitoParser import PequePatitoParser

class PequePatitoListener(ParseTreeListener):
    def __init__(self, cubo_semantico, tabla_variables, directorio_funciones):
        self.cubo_semantico = cubo_semantico
        self.tabla_variables = tabla_variables
        self.directorio_funciones = directorio_funciones
        self.ambito_actual = "global"
        self.pila_scopes = ["global"]
        self.errores = []

        self.pilas = PilasCuadruplos()
        self.fila_cuadruplos = FilaCuadruplos()

        self.cont_temp = 0

    def generar_temporal(self):
        temp = f"t{self.cont_temp}"
        self.cont_temp += 1
        return temp

    # Método para detectar y manejar operadores
    def visitTerminal(self, node: TerminalNode):
        token_type = node.getSymbol().type
        if token_type in [
            PequePatitoParser.SUMA,
            PequePatitoParser.RESTA,
            PequePatitoParser.MULTIPLICACION,
            PequePatitoParser.DIVISION,
            PequePatitoParser.MAYOR,
            PequePatitoParser.MENOR,
            PequePatitoParser.IGUAL,
            PequePatitoParser.DIFERENTE,
            PequePatitoParser.AND,
            PequePatitoParser.OR,
            PequePatitoParser.NOT
        ]:
            operador = node.getText()
            self.pilas.push_operador(operador)

    # Métodos para manejar declaraciones de variables
    def enterVar_declaracion(self, ctx: PequePatitoParser.Var_declaracionContext):
        scope_actual = self.pila_scopes[-1]
        variables = ctx.id_list().ID()
        tipo = ctx.tipo().getText()

        for var in variables:
            nombre_var = var.getText()
            if nombre_var in self.tabla_variables.variables[scope_actual]:
                self.errores.append(
                    f"Error: Variable '{nombre_var}' ya declarada en el ámbito '{scope_actual}'.")
            else:
                self.tabla_variables.agregar_variable(nombre_var, tipo, scope_actual)
                if scope_actual == "global":
                    self.directorio_funciones.funciones["global"]["variables_locales"][nombre_var] = {'tipo': tipo}
                else:
                    self.directorio_funciones.funciones[scope_actual]["variables_locales"][nombre_var] = {'tipo': tipo}
            print(f"Declaración de variable '{nombre_var}' de tipo '{tipo}' en ámbito '{scope_actual}'")

    # Métodos para manejar expresiones
    def exitF_otro(self, ctx: PequePatitoParser.F_otroContext):
        valor = ctx.getText()
        if valor.startswith('-') or valor.startswith('+'):
            signo = valor[0]
            var = valor[1:]
            self.pilas.push_operando(valor)
            self.pilas.push_tipo('entero')
        else:
            if ctx.ID():
                var = ctx.ID().getText()
                self.pilas.push_operando(var)
                tipo = self.tabla_variables.obtener_tipo_variable(var, self.ambito_actual)
                if tipo is None:
                    self.errores.append(f"Error: Variable '{var}' no declarada.")
                    tipo = 'error'
                self.pilas.push_tipo(tipo)
            elif ctx.cte():
                if ctx.cte().CTE_ENT():
                    const = ctx.cte().CTE_ENT().getText()
                    self.pilas.push_operando(const)
                    self.pilas.push_tipo('entero')
                elif ctx.cte().CTE_FLOT():
                    const = ctx.cte().CTE_FLOT().getText()
                    self.pilas.push_operando(const)
                    self.pilas.push_tipo('flotante')
                elif ctx.cte().VERDADERO():
                    const = ctx.cte().VERDADERO().getText()
                    self.pilas.push_operando(const)
                    self.pilas.push_tipo('booleano')
                elif ctx.cte().FALSO():
                    const = ctx.cte().FALSO().getText()
                    self.pilas.push_operando(const)
                    self.pilas.push_tipo('booleano')

    def exitTermino(self, ctx: PequePatitoParser.TerminoContext):
        while self.pilas.pila_operadores and self.pilas.pila_operadores[-1] in ['*', '/']:
            operador = self.pilas.pop_operador()
            operando_derecho = self.pilas.pop_operando()
            tipo_derecho = self.pilas.pop_tipo()
            operando_izquierdo = self.pilas.pop_operando()
            tipo_izquierdo = self.pilas.pop_tipo()

            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo_izquierdo, tipo_derecho, operador)
            if tipo_resultado == 'error':
                self.errores.append(f"Error de tipos: No se puede aplicar operador '{operador}' a tipos '{tipo_izquierdo}' y '{tipo_derecho}'.")

            temp = self.generar_temporal()
            self.fila_cuadruplos.agregar_cuadruplo(operador, operando_izquierdo, operando_derecho, temp)
            self.pilas.push_operando(temp)
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
                self.errores.append(f"Error de tipos: No se puede aplicar operador '{operador}' a tipos '{tipo_izquierdo}' y '{tipo_derecho}'.")

            temp = self.generar_temporal()
            self.fila_cuadruplos.agregar_cuadruplo(operador, operando_izquierdo, operando_derecho, temp)
            self.pilas.push_operando(temp)
            self.pilas.push_tipo(tipo_resultado)

    def exitBo(self, ctx: PequePatitoParser.BoContext):
        if ctx.op_relacional():
            operador = self.pilas.pop_operador()
            operando_derecho = self.pilas.pop_operando()
            tipo_derecho = self.pilas.pop_tipo()
            operando_izquierdo = self.pilas.pop_operando()
            tipo_izquierdo = self.pilas.pop_tipo()

            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo_izquierdo, tipo_derecho, operador)
            if tipo_resultado == 'error':
                self.errores.append(f"Error de tipos: No se puede aplicar operador relacional '{operador}' a tipos '{tipo_izquierdo}' y '{tipo_derecho}'.")

            temp = self.generar_temporal()
            self.fila_cuadruplos.agregar_cuadruplo(operador, operando_izquierdo, operando_derecho, temp)
            self.pilas.push_operando(temp)
            self.pilas.push_tipo(tipo_resultado)

    def exitLogica(self, ctx: PequePatitoParser.LogicaContext):
        if ctx.op_logico():
            operador = self.pilas.pop_operador()
            operando_derecho = self.pilas.pop_operando()
            tipo_derecho = self.pilas.pop_tipo()
            operando_izquierdo = self.pilas.pop_operando()
            tipo_izquierdo = self.pilas.pop_tipo()

            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo_izquierdo, tipo_derecho, operador)
            if tipo_resultado == 'error':
                self.errores.append(f"Error de tipos: No se puede aplicar operador lógico '{operador}' a tipos '{tipo_izquierdo}' y '{tipo_derecho}'.")

            temp = self.generar_temporal()
            self.fila_cuadruplos.agregar_cuadruplo(operador, operando_izquierdo, operando_derecho, temp)
            self.pilas.push_operando(temp)
            self.pilas.push_tipo(tipo_resultado)
        elif ctx.NOT():
            operador = self.pilas.pop_operador()
            operando = self.pilas.pop_operando()
            tipo = self.pilas.pop_tipo()

            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo, None, operador)
            if tipo_resultado == 'error':
                self.errores.append(f"Error de tipos: No se puede aplicar operador lógico '{operador}' a tipo '{tipo}'.")

            temp = self.generar_temporal()
            self.fila_cuadruplos.agregar_cuadruplo(operador, operando, None, temp)
            self.pilas.push_operando(temp)
            self.pilas.push_tipo(tipo_resultado)

    # Métodos para manejar asignaciones
    def exitAsigna(self, ctx: PequePatitoParser.AsignaContext):
        var_destino = ctx.ID().getText()
        expr_result = self.pilas.pop_operando()
        expr_tipo = self.pilas.pop_tipo()

        var_tipo = self.tabla_variables.obtener_tipo_variable(var_destino, self.ambito_actual)
        if var_tipo is None:
            self.errores.append(f"Error: Variable '{var_destino}' no declarada.")
            var_tipo = 'error'

        tipo_resultado = self.cubo_semantico.obtener_tipo(var_tipo, expr_tipo, '=')
        if tipo_resultado == 'error':
            self.errores.append(f"Error de tipos: No se puede asignar tipo '{expr_tipo}' a variable '{var_destino}' de tipo '{var_tipo}'.")

        self.fila_cuadruplos.agregar_cuadruplo('=', expr_result, None, var_destino)

    # Métodos para manejar sentencias de impresión
    def exitImprime(self, ctx: PequePatitoParser.ImprimeContext):
        p_imp = ctx.p_imp()
        args = []
        for arg in p_imp.children:
            if arg.getText() == ',':
                continue
            if isinstance(arg, PequePatitoParser.ExpresionContext):
                expr_result = self.pilas.pop_operando()
                args.append(expr_result)
            else:
                if arg.symbol.type == PequePatitoParser.LETRERO:
                    cadena = arg.getText()
                    args.append(cadena)
                elif arg.symbol.type == PequePatitoParser.VERDADERO:
                    args.append("verdadero")
                elif arg.symbol.type == PequePatitoParser.FALSO:
                    args.append("falso")
                elif arg.symbol.type == PequePatitoParser.ID:
                    var = arg.getText()
                    args.append(var)

        for arg in args:
            self.fila_cuadruplos.agregar_cuadruplo('print', arg, None, None)

    # Métodos para manejar sentencias condicionales
    def enterCondicion(self, ctx: PequePatitoParser.CondicionContext):
        pass  # Nada que hacer al entrar a la condición

    def exitCondicion(self, ctx: PequePatitoParser.CondicionContext):
        resultado_condicion = self.pilas.pop_operando()
        tipo_condicion = self.pilas.pop_tipo()

        if tipo_condicion != 'booleano':
            self.errores.append(f"Error: La condición debe ser de tipo booleano, pero es '{tipo_condicion}'.")

        self.fila_cuadruplos.agregar_cuadruplo('if_false', resultado_condicion, None, None)
        salto_false = len(self.fila_cuadruplos.cuadruplos) - 1
        self.pilas.push_salto(salto_false)

        if ctx.else_part():
            self.fila_cuadruplos.agregar_cuadruplo('goto', None, None, None)
            salto_goto = len(self.fila_cuadruplos.cuadruplos) - 1
            self.pilas.push_salto(salto_goto)

            salto_false = self.pilas.pop_salto()
            self.fila_cuadruplos.cuadruplos[salto_false] = ('if_false', resultado_condicion, None, len(self.fila_cuadruplos.cuadruplos))

            # El código del bloque 'sino' se genera aquí durante el recorrido del árbol

            salto_goto = self.pilas.pop_salto()
            self.fila_cuadruplos.cuadruplos[salto_goto] = ('goto', None, None, len(self.fila_cuadruplos.cuadruplos))
        else:
            salto_false = self.pilas.pop_salto()
            self.fila_cuadruplos.cuadruplos[salto_false] = ('if_false', resultado_condicion, None, len(self.fila_cuadruplos.cuadruplos))
