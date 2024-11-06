# peque_patito_listener.py

from antlr4 import ParseTreeListener, TerminalNode
from pilas_cuadruplos import PilasCuadruplos
from fila_cuadruplos import FilaCuadruplos
from gen.PequePatitoParser import PequePatitoParser  # Asegúrate de que el path sea correcto

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
        self.cont_label = 0

        # Variables para manejo de condiciones
        self.en_condicion = False
        self.label_sino = ""
        self.label_fin = ""

    def generar_temporal(self):
        temp = f"t{self.cont_temp}"
        self.cont_temp += 1
        return temp

    def generar_label(self):
        label = f"L{self.cont_label}"
        self.cont_label += 1
        return label

    # Método para detectar y manejar operadores
    def visitTerminal(self, node: TerminalNode):
        token_type = node.getSymbol().type
        if token_type in [
            PequePatitoParser.SUMA,           # Operador Aritmético: +
            PequePatitoParser.RESTA,          # Operador Aritmético: -
            PequePatitoParser.MULTIPLICACION, # Operador Aritmético: *
            PequePatitoParser.DIVISION,       # Operador Aritmético: /
            PequePatitoParser.MAYOR,          # Operador Relacional: >
            PequePatitoParser.MENOR,          # Operador Relacional: <
            PequePatitoParser.IGUAL,          # Operador Relacional: ==
            PequePatitoParser.DIFERENTE,      # Operador Relacional: !=
            PequePatitoParser.AND,            # Operador Lógico: &&
            PequePatitoParser.OR,             # Operador Lógico: ||
            PequePatitoParser.NOT             # Operador Lógico: !
        ]:
            operador = node.getText()
            self.pilas.push_operador(operador)

    # Métodos para la regla inicial del programa
    def enterPrograma(self, ctx: PequePatitoParser.ProgramaContext):
        print("Inicio del programa.")

    def exitPrograma(self, ctx: PequePatitoParser.ProgramaContext):
        print("Fin del programa.")

    # Métodos para manejar declaraciones de variables
    def enterVar_declaracion(self, ctx: PequePatitoParser.Var_declaracionContext):
        """
        Procesa las declaraciones de variables en el ámbito actual y asegura que cada variable se registre.
        """
        scope_actual = self.pila_scopes[-1]  # Obtener el scope actual desde la pila
        variables = ctx.id_list().ID()  # Lista de variables declaradas en esta instrucción
        tipo = ctx.tipo().getText()  # Tipo de las variables

        for var in variables:
            nombre_var = var.getText()  # Obtener el texto del ID
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

    # Métodos para manejar expresiones
    def exitF_otro(self, ctx: PequePatitoParser.F_otroContext):
        """
        Se invoca al salir de la regla f_otro.
        Procesa factores simples: ID, constantes, con posible signo.
        """
        valor = ctx.getText()
        if valor.startswith('-') or valor.startswith('+'):
            signo = valor[0]
            var = valor[1:]
            # Manejar signo si es necesario
            # Por simplicidad, consideramos solo el valor
            self.pilas.push_operando(var)
            # Tipo debería estar determinado previamente
            tipo = self.tabla_variables.obtener_tipo_variable(var, self.ambito_actual)
            if tipo is None:
                self.errores.append(f"Error: Variable '{var}' no declarada.")
                tipo = 'error'
            self.pilas.push_tipo(tipo)
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
        """
        Se invoca al salir de la regla termino.
        Maneja multiplicación y división.
        """
        while self.pilas.pila_operadores and self.pilas.pila_operadores[-1] in ['*', '/']:
            operador = self.pilas.pop_operador()
            operando2 = self.pilas.pop_operando()
            tipo2 = self.pilas.pop_tipo()
            operando1 = self.pilas.pop_operando()
            tipo1 = self.pilas.pop_tipo()

            # Verificar tipos usando el cubo semántico
            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo1, tipo2, operador)
            if tipo_resultado == 'error':
                self.errores.append(f"Error de tipos: No se puede aplicar operador '{operador}' a tipos '{tipo1}' y '{tipo2}'.")
                tipo_resultado = 'error'

            temp = self.generar_temporal()
            self.fila_cuadruplos.agregar_cuadruplo(operador, operando1, operando2, temp)

            # Push del resultado en las pilas
            self.pilas.push_operando(temp)
            self.pilas.push_tipo(tipo_resultado)

    def exitExpresion(self, ctx: PequePatitoParser.ExpresionContext):
        """
        Se invoca al salir de la regla expresion.
        Maneja suma y resta.
        """
        while self.pilas.pila_operadores and self.pilas.pila_operadores[-1] in ['+', '-']:
            operador = self.pilas.pop_operador()
            operando2 = self.pilas.pop_operando()
            tipo2 = self.pilas.pop_tipo()
            operando1 = self.pilas.pop_operando()
            tipo1 = self.pilas.pop_tipo()

            # Verificar tipos usando el cubo semántico
            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo1, tipo2, operador)
            if tipo_resultado == 'error':
                self.errores.append(f"Error de tipos: No se puede aplicar operador '{operador}' a tipos '{tipo1}' y '{tipo2}'.")
                tipo_resultado = 'error'

            temp = self.generar_temporal()
            self.fila_cuadruplos.agregar_cuadruplo(operador, operando1, operando2, temp)

            # Push del resultado en las pilas
            self.pilas.push_operando(temp)
            self.pilas.push_tipo(tipo_resultado)

    def exitBo(self, ctx: PequePatitoParser.BoContext):
        """
        Se invoca al salir de la regla bo.
        Maneja expresiones relacionales.
        """
        if ctx.op_relacional():
            operador = ctx.op_relacional().getText()  # '>', '<', '==', '!='
            operando2 = self.pilas.pop_operando()
            tipo2 = self.pilas.pop_tipo()
            operando1 = self.pilas.pop_operando()
            tipo1 = self.pilas.pop_tipo()

            # Verificar tipos usando el cubo semántico
            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo1, tipo2, operador)
            if tipo_resultado == 'error':
                self.errores.append(f"Error de tipos: No se puede aplicar operador relacional '{operador}' a tipos '{tipo1}' y '{tipo2}'.")
                tipo_resultado = 'error'

            temp = self.generar_temporal()
            self.fila_cuadruplos.agregar_cuadruplo(operador, operando1, operando2, temp)

            # Push del resultado booleano en las pilas
            self.pilas.push_operando(temp)
            self.pilas.push_tipo(tipo_resultado)

            # Si estamos en una condición, generar los saltos condicionales aquí
            if self.en_condicion:
                self.label_sino = self.generar_label()
                self.label_fin = self.generar_label()

                # Cuádruplo para saltar si la condición es falsa
                self.fila_cuadruplos.agregar_cuadruplo('if_false', temp, None, self.label_sino)

                # Cuádruplo para saltar al fin después del bloque 'si'
                self.fila_cuadruplos.agregar_cuadruplo('goto', None, None, self.label_fin)

                # Resetear la bandera de condición
                self.en_condicion = False

    def exitLogica(self, ctx: PequePatitoParser.LogicaContext):
        """
        Se invoca al salir de la regla logica.
        Maneja operadores lógicos y operaciones NOT.
        """
        if ctx.op_logico():
            # Operación lógica binaria (&&, ||)
            operador = ctx.op_logico().getText()  # '&&', '||'
            operando2 = self.pilas.pop_operando()
            tipo2 = self.pilas.pop_tipo()
            operando1 = self.pilas.pop_operando()
            tipo1 = self.pilas.pop_tipo()

            # Verificar tipos usando el cubo semántico
            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo1, tipo2, operador)
            if tipo_resultado == 'error':
                self.errores.append(f"Error de tipos: No se puede aplicar operador lógico '{operador}' a tipos '{tipo1}' y '{tipo2}'.")
                tipo_resultado = 'error'

            temp = self.generar_temporal()
            self.fila_cuadruplos.agregar_cuadruplo(operador, operando1, operando2, temp)

            # Push del resultado booleano en las pilas
            self.pilas.push_operando(temp)
            self.pilas.push_tipo(tipo_resultado)
        elif ctx.NOT():
            # Operación lógica unaria (NOT)
            operador = '!'
            operando = self.pilas.pop_operando()
            tipo = self.pilas.pop_tipo()

            # Verificar tipos usando el cubo semántico
            tipo_resultado = self.cubo_semantico.obtener_tipo(tipo, None, operador)
            if tipo_resultado == 'error':
                self.errores.append(f"Error de tipos: No se puede aplicar operador lógico '{operador}' a tipo '{tipo}'.")
                tipo_resultado = 'error'

            temp = self.generar_temporal()
            self.fila_cuadruplos.agregar_cuadruplo(operador, operando, None, temp)

            # Push del resultado booleano en las pilas
            self.pilas.push_operando(temp)
            self.pilas.push_tipo(tipo_resultado)

    # Métodos para manejar asignaciones
    def exitAsigna(self, ctx: PequePatitoParser.AsignaContext):
        """
        Se invoca al salir de una asignación.
        Genera el cuádruplo de asignación.
        """
        var_destino = ctx.ID().getText()
        expr_result = self.pilas.pop_operando()
        expr_tipo = self.pilas.pop_tipo()

        # Obtener el tipo de la variable destino
        var_tipo = self.tabla_variables.obtener_tipo_variable(var_destino, self.ambito_actual)
        if var_tipo is None:
            self.errores.append(f"Error: Variable '{var_destino}' no declarada.")
            var_tipo = 'error'

        # Verificar tipos usando el cubo semántico con el operador '='
        tipo_resultado = self.cubo_semantico.obtener_tipo(var_tipo, expr_tipo, '=')
        if tipo_resultado == 'error':
            self.errores.append(f"Error de tipos: No se puede asignar tipo '{expr_tipo}' a variable '{var_destino}' de tipo '{var_tipo}'.")

        # Generar el cuádruplo de asignación
        self.fila_cuadruplos.agregar_cuadruplo('=', expr_result, None, var_destino)

    # Métodos para manejar sentencias de impresión
    def exitImprime(self, ctx: PequePatitoParser.ImprimeContext):
        """
        Se invoca al salir de una sentencia de impresión.
        Genera los cuádruplos de impresión.
        """
        # Obtener los argumentos a imprimir
        p_imp = ctx.p_imp()
        args = []
        # Recorremos cada argumento
        for arg in p_imp.children:
            if arg.getText() == ',':
                continue
            if isinstance(arg, PequePatitoParser.ExpresionContext):
                # Es una expresión
                expr_result = self.pilas.pop_operando()
                expr_tipo = self.pilas.pop_tipo()
                args.append(expr_result)
            else:
                # Es un terminal: LETRERO, VERDADERO, FALSO
                if arg.symbol.type == PequePatitoParser.LETRERO:
                    cadena = arg.getText().strip('"')
                    args.append(f'"{cadena}"')
                elif arg.symbol.type == PequePatitoParser.VERDADERO:
                    args.append("verdadero")
                elif arg.symbol.type == PequePatitoParser.FALSO:
                    args.append("falso")
                elif arg.symbol.type == PequePatitoParser.ID:
                    var = arg.getText()
                    args.append(var)

        # Generar un único cuádruplo de impresión con todos los argumentos
        # Para simplificar, concatenamos los argumentos en una cadena de impresión
        concatenado = ' + '.join(args)  # Asumiendo que '+' puede concatenar cadenas
        self.fila_cuadruplos.agregar_cuadruplo('print', concatenado, None, None)

    # Métodos para manejar sentencias condicionales
    def enterCondicion(self, ctx: PequePatitoParser.CondicionContext):
        """
        Se invoca al entrar a una sentencia condicional si-sino.
        """
        self.en_condicion = True  # Indica que estamos dentro de una condición

    def exitCondicion(self, ctx: PequePatitoParser.CondicionContext):
        """
        Se invoca al salir de la regla condicion.
        Genera las etiquetas para el bloque 'sino' y el fin de la condición.
        """
        # Generar etiquetas
        self.fila_cuadruplos.agregar_cuadruplo('label', None, None, self.label_sino)
        self.fila_cuadruplos.agregar_cuadruplo('label', None, None, self.label_fin)
