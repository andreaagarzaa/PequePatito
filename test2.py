# test.py

import sys
from antlr4 import *
from gen.PequePatitoLexer import PequePatitoLexer
from gen.PequePatitoParser import PequePatitoParser
from cubo_semantico import CuboSemantico
from estructura_directorio import TablaVariables, DirectorioFunciones
from peque_patito_listener import PequePatitoListener
from fila_cuadruplos import FilaCuadruplos


def run_test(programa, test_number):
    print(f"\n=== Ejecutando Prueba {test_number} ===")
    print("Programa PATITO:\n")
    print(programa)
    print("\n--- Análisis Léxico y Sintáctico ---")

    try:
        input_stream = InputStream(programa)
        lexer = PequePatitoLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = PequePatitoParser(stream)

        # Añadir un error listener personalizado para capturar errores de sintaxis
        from antlr4.error.ErrorListener import ErrorListener

        class MyErrorListener(ErrorListener):
            def __init__(self):
                super(MyErrorListener, self).__init__()
                self.errors = []

            def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
                self.errors.append(f"Error de sintaxis en línea {line}, columna {column}: {msg}")

        error_listener = MyErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        # Crear el árbol de sintaxis
        tree = parser.programa()

        # Verificar si hay errores de sintaxis
        if error_listener.errors:
            print("Errores de sintaxis encontrados:")
            for error in error_listener.errors:
                print(error)
            return False, None

        # Crear instancias de las estructuras de datos
        cubo_semantico = CuboSemantico()
        tabla_variables = TablaVariables()
        directorio_funciones = DirectorioFunciones()

        # Crear el listener y recorrer el árbol
        listener = PequePatitoListener(cubo_semantico, tabla_variables, directorio_funciones)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        # Verificar si hay errores semánticos
        if listener.errores:
            print("Errores semánticos encontrados:")
            for error in listener.errores:
                print(error)
            return False, None
        else:
            print("Análisis semántico completado sin errores.\n")

        # Imprimir la tabla de variables y el directorio de funciones
        print("--- Tabla de Variables ---")
        tabla_variables.imprimir_tabla()
        print("\n--- Directorio de Funciones ---")
        directorio_funciones.imprimir_directorio()

        # Imprimir la fila de cuadruplos
        print("\n--- Cuádruplos Generados ---")
        listener.fila_cuadruplos.imprimir_cuadruplos()

        return True, listener.fila_cuadruplos.cuadruplos

    except Exception as e:
        print(f"Error durante el análisis léxico/sintáctico: {e}")
        return False, None


def main():
    # Definir una lista de programas de prueba en PATITO
    programas_de_prueba = [
        # Prueba 1: Asignaciones simples y operaciones aritméticas
        """
        programa ejemplo1;
        vars
            a, b, c : entero;

        inicio{
            a = 5;
            b = a + 10;
            c = b * 2;
            escribe("El valor de c es: ", c);
        }fin
        """,

        # Prueba 2: Uso de variables flotantes y operaciones mixtas
        """
        programa ejemplo2;
        vars
            x, y, z : flotante;

        inicio{
            x = 3.5;
            y = x * 2;
            z = y + x / 2;
            escribe("El valor de z es: ", z);
        }fin
        """,

        # Prueba 3: Condicionales sin 'sino'
        #marca error en Error durante el análisis léxico/sintáctico: Error: Pila de operandos vacía. CHECAR

        """
        programa ejemplo3;
        vars
            num : entero;
            flag : booleano;

        inicio{
            num = 10;
            flag = verdadero;
            si (num > 5 && flag) {
                escribe("num es mayor que 5 y flag es verdadero");
            };
        }fin
        """,

        # Prueba 4: Condicionales con 'sino'
        # marca error en Error durante el análisis léxico/sintáctico: Error: Pila de operandos vacía. CHECAR

        """
        programa ejemplo4;
        vars
            a, b : entero;
            flag : booleano;

        inicio{
            a = 3;
            b = 7;
            flag = falso;
            si (a < b || flag) {
                escribe("a es menor que b o flag es verdadero");
            } sino {
                escribe("a no es menor que b y flag es falso");
            };
        }fin
        """,

        # Prueba 5: Ciclos mientras-haz
        # CHEACR ERROR :Error: La condición del ciclo debe ser de tipo booleano, pero es de tipo 'entero'.
        """
        programa ejemplo5;
        vars
            i, total : entero;

        inicio{
            i = 0;
            total = 0;
            mientras (i < 5) haz {
                total = total + i;
                escribe("Valor de i:", i);
                i = i + 1;
            };
            escribe("Total:", total);
        }fin
        """,

        # Prueba 6: Funciones y llamadas
        #CHECAR Error de sintaxis en línea 6, columna 20: mismatched input ',' expecting ':'

        """
        programa ejemplo6;
        vars
            resultado : entero;

        nula sumar(c, d : entero) {
            vars
                temp : entero;
            {
                temp = c + d;
                escribe("La suma es:", temp);
            }
        };

        inicio{
            resultado = 0;
            sumar(5, 10);
            escribe("Resultado:", resultado);
        }fin
        """,

        # Prueba 7: Errores semánticos (variable no declarada)
        """
        programa ejemplo7;
        vars
            a : entero;

        inicio{
            a = 10;
            b = a + 5; // 'b' no está declarada
            escribe("Valor de b:", b);
        }fin
        """,

        # Prueba 8: Errores semánticos (tipos incompatibles)
        """
        programa ejemplo8;
        vars
            a : entero;
            b : flotante;

        inicio{
            a = 5.5; // Asignación de flotante a entero
            b = a + "texto"; // Operación inválida
            escribe("Valor de a:", a);
            escribe("Valor de b:", b);
        }fin
        """,

        # Prueba 9: Uso de operadores unarios
        #CHECAR ERROR :Error durante el análisis léxico/sintáctico: Error: Pila de operandos vacía.

        """
        programa ejemplo9;
        vars
            a : entero;
            b : booleano;

        inicio{
            a = -5;
            b = !verdadero;
            escribe("Valor de a:", a);
            escribe("Valor de b:", b);
        }fin
        """,

        # Prueba 10: Ciclo anidado
        #ERRORES: Errores semánticos encontrados:
#Error: La condición del ciclo debe ser de tipo booleano, pero es de tipo 'entero'.
#Error: La condición del ciclo debe ser de tipo booleano, pero es de tipo 'entero'.
        """
        programa ejemplo10;
        vars
            i, j, total : entero;

        inicio{
            i = 0;
            total = 0;
            mientras (i < 3) haz {
                j = 0;
                mientras (j < 2) haz {
                    total = total + i + j;
                    escribe("i:", i, "j:", j);
                    j = j + 1;
                };
                i = i + 1;
            };
            escribe("Total:", total);
        }fin
        """
    ]

    total_pruebas = len(programas_de_prueba)
    exitos = 0
    fallidos = 0

    for idx, programa in enumerate(programas_de_prueba, start=1):
        exito, cuadruplos = run_test(programa, idx)
        if exito:
            exitos += 1
        else:
            fallidos += 1

    print("\n=== Resumen de Pruebas ===")
    print(f"Total de pruebas: {total_pruebas}")
    print(f"Pruebas exitosas: {exitos}")
    print(f"Pruebas fallidas: {fallidos}")


if __name__ == "__main__":
    main()
