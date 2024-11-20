# test.py
import sys
from antlr4 import *
from gen.PequePatitoLexer import PequePatitoLexer
from gen.PequePatitoParser import PequePatitoParser
from cubo_semantico import CuboSemantico
from estructura_directorio import TablaVariables, DirectorioFunciones
from maquina_virtual import MaquinaVirtual
from peque_patito_listener import PequePatitoListener
#from maquina_virtual import MaquinaVirtual
import traceback

programa = '''
programa miPrograma;
vars
    x, y : entero;
    z : flotante;
    holi: entero;

nula miFuncion(c: entero, a: entero) {
    vars
        pi: flotante;
    {
        pi = 3.14;
        c = a + 10;
        escribe("El valor de c es: ", c);
    }
};

inicio{
    x = 10;
    y = 20;
    z = x + y * 1.5;
    si (x > y) {
        escribe("x es mayor que y");
    } sino {
        escribe("y es mayor o igual que x");
    };
    mientras (x < 50) haz {
        holi = 3;
        x = x + 5;
        escribe("x ahora es: ", x);
    };
    miFuncion(x, y);
}fin
'''

try:
    # Preparar el input para ANTLR
    input_stream = InputStream(programa)
    lexer = PequePatitoLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PequePatitoParser(stream)

    # Verificar si hay errores de sintaxis
    if parser.getNumberOfSyntaxErrors() > 0:
        print("Error: Se encontraron errores de sintaxis en el archivo.")
        sys.exit(1)

    # Crear el árbol de sintaxis
    tree = parser.programa()

    # Crear instancias de las estructuras de datos
    cubo_semantico = CuboSemantico()
    tabla_variables = TablaVariables()
    directorio_funciones = DirectorioFunciones()

    # Crear el listener y recorrer el árbol
    listener = PequePatitoListener(cubo_semantico, tabla_variables, directorio_funciones)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    # Verificar si hay errores semánticos
    if hasattr(listener, "errores") and listener.errores:
        for error in listener.errores:
            print(error)
        sys.exit(1)
    else:
        print("Análisis semántico completado sin errores.\n")

    # Imprimir la tabla de variables y el directorio de funciones
    print("\n--- Resultado Final ---")
    tabla_variables.imprimir_tabla()
    directorio_funciones.imprimir_directorio()

    # Imprimir la tabla de constantes
    listener.tabla_constantes.imprimir_constantes()

    # Imprimir la fila de cuadruplos
    listener.fila_cuadruplos.imprimir_cuadruplos()

     # Ejecutar la máquina virtual
    print("\n--- Ejecución de la Máquina Virtual ---")
    vm = MaquinaVirtual(listener.fila_cuadruplos.cuadruplos, listener.tabla_constantes, tabla_variables)
    vm.ejecutar()

except Exception as e:
    print(f"Error durante el análisis léxico/sintáctico: {e}")
    traceback.print_exc()
    sys.exit(1)
