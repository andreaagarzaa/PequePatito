# test.py

import sys
from antlr4 import *
from gen.PequePatitoLexer import PequePatitoLexer
from gen.PequePatitoParser import PequePatitoParser
from cubo_semantico import CuboSemantico
from estructura_directorio import TablaVariables, DirectorioFunciones
from maquina_virtual import MaquinaVirtual
from peque_patito_listener import PequePatitoListener
import traceback

# Definición de los casos de prueba
test_cases = [
    {
        "name": "Test Scope - Variables Globales y Locales con el Mismo Nombre",
        "description": "Verifica que las variables locales en una función no interfieran con las variables globales que tienen el mismo nombre.",
        "code": '''
        programa TestScope;
        vars
            x: entero;

        nula setX(newX: entero) {
            vars
                x: entero;
            {
                x = newX;
                escribe("Valor de x dentro de setX: ", x);
            }
        };

        inicio{
            x = 10;
            escribe("Valor de x antes de llamar a setX: ", x);
            setX(20);
            escribe("Valor de x después de llamar a setX: ", x);
        }fin
        '''
    },
    {
        "name": "Test Undefined Variable",
        "description": "Intenta usar una variable que no ha sido declarada para verificar que el compilador detecte y reporte el error correctamente.",
        "code": '''
        programa TestUndefinedVar;
        vars
            a: entero;

        inicio{
            a = 5;
            b = 10; // 'b' no ha sido declarada
        }fin
        '''
    },
    {
        "name": "Test Function Call with Incorrect Parameter Count",
        "description": "Llama a una función pasando más parámetros de los que espera.",
        "code": '''
        programa TestFuncParams;
        vars
            a: entero;

        nula printSum(x: entero, y: entero) {
            vars
                sum: entero;
            {
                sum = x + y;
                escribe("Suma: ", sum);
            }
        };

        inicio{
            a = 10;
            printSum(a, 20, 30); // Demasiados parámetros
        }fin
        '''
    },
    {
        "name": "Test Function Call with Incorrect Parameter Types",
        "description": "Llama a una función pasando parámetros de tipos diferentes a los que espera.",
        "code": '''
        programa TestFuncParamTypes;
        vars
            a: entero;

        nula printSum(x: entero, y: entero) {
            vars
                sum: entero;
            {
                sum = x + y;
                escribe("Suma: ", sum);
            }
        };

        inicio{
            a = 10;
            printSum(a, "veinte"); // Tipo incorrecto para 'y'
        }fin
        '''
    },
    {
        "name": "Test Function Call Without Parameters",
        "description": "Llama a una función que espera parámetros pero no le pasa ninguno.",
        "code": '''
        programa TestFuncNoParams;
        vars
            a: entero;

        nula printSum(x: entero, y: entero) {
            vars
                sum: entero;
            {
                sum = x + y;
                escribe("Suma: ", sum);
            }
        };

        inicio{
            a = 10;
            printSum(); // Faltan parámetros
        }fin
        '''
    },
    {
        "name": "Test Complex Conditions",
        "description": "Usa condiciones complejas en 'si' y 'mientras' para verificar el manejo correcto de operadores lógicos y relacionales.",
        "code": '''
        programa TestComplexConditions;
        vars
            a, b: entero;

        nula checkConditions(x: entero, y: entero) {
            si (x > y && x < 100 || y == 20) {
                escribe("Condición verdadera");
            } sino {
                escribe("Condición falsa");
            };
        };

        inicio{
            a = 50;
            b = 20;
            checkConditions(a, b);
        }fin
        '''
    },
    {
        "name": "Test Infinite Loop Detection",
        "description": "Crea un ciclo 'mientras' que nunca cumple la condición de terminación para verificar que tu máquina virtual maneje adecuadamente la terminación de ciclos.",
        "code": '''
        programa TestInfiniteLoop;
        vars
            i: entero;

        nula mainLoop() {
            vars
                i: entero;
            {
                i = 0;
                mientras (i < 5) haz {
                    escribe("i: ", i);
                    i = i + 1;
                };
            }
        };

        inicio{
            mainLoop();
        }fin
        '''
    },
    {
        "name": "Test Type Mismatch",
        "description": "Intenta asignar un valor de tipo diferente al declarado para una variable para verificar que el compilador detecte errores de tipo.",
        "code": '''
        programa TestTypeMismatch;
        vars
            a: entero;

        inicio{
            a = "veinte"; // Asignación de cadena a entero
        }fin
        '''
    },
    {
        "name": "Test Mixed Type Operations",
        "description": "Realiza operaciones entre diferentes tipos de datos (e.g., entero y flotante) para verificar que el cubo semántico maneje correctamente las conversiones y operaciones.",
        "code": '''
        programa TestMixedTypes;
        vars
            a: entero;
            b: flotante;
            c: flotante;

        inicio{
            a = 10;
            b = 3.5;
            c = a + b; // Operación entre entero y flotante
            escribe("Resultado: ", c);
        }fin
        '''
    },
    {
        "name": "Test Invalid Operation with Strings",
        "description": "Intenta realizar operaciones aritméticas con cadenas para verificar que el compilador detecte y reporte el error.",
        "code": '''
        programa TestInvalidOperation;
        vars
            a: entero;
            b: cadena;
            c: entero;

        inicio{
            a = 10;
            b = "10";
            c = a + b; // Operación inválida
        }fin
        '''
    },
    {
        "name": "Test Function Recursion",
        "description": "Implementa una función recursiva (e.g., cálculo de factorial) para verificar que la máquina virtual maneje correctamente las llamadas recursivas y la pila de contextos.",
        "code": '''
        programa TestRecursion;
        vars
            n: entero;
            result: entero;

        nula factorial(x: entero) {
            vars
                temp: entero;
            {
                si (x == 0) {
                    result = 1;
                } sino {
                    factorial(x - 1);
                    result = x * result;
                };
            }
        };

        inicio{
            n = 5;
            factorial(n);
            escribe("Factorial de ", n, " es ", result);
        }fin
        '''
    },
    {
        "name": "Test Nested Functions",
        "description": "Crea funciones dentro de otras funciones para verificar que el compilador y la máquina virtual manejen correctamente el alcance y las llamadas.",
        "code": '''
        programa TestNestedFunctions;
        vars
            a: entero;

        nula innerFunction(x: entero) {
            vars
                result: entero;
            {
                result = x * 2;
                escribe("Resultado en innerFunction: ", result);
            }
        };

        nula outerFunction(y: entero) {
            vars
                z: entero;
            {
                z = y + 5;
                escribe("Valor en outerFunction: ", z);
                innerFunction(z);
            }
        };

        inicio{
            a = 10;
            outerFunction(a);
        }fin
        '''
    },
    {
        "name": "Test Division by Zero",
        "description": "Realiza una operación de división donde el divisor es cero para verificar que se maneje correctamente el error.",
        "code": '''
        programa TestDivisionByZero;
        vars
            a: entero;
            b: entero;
            c: flotante;

        inicio{
            a = 10;
            b = 0;
            c = a / b; // División por cero
            escribe("Resultado: ", c);
        }fin
        '''
    },
    {
        "name": "Test Undefined Function Call",
        "description": "Intenta llamar a una función que no ha sido definida para verificar que el compilador detecte y reporte el error.",
        "code": '''
        programa TestUndefinedFunction;
        vars
            a: entero;

        inicio{
            a = 10;
            undefinedFunction(a); // Función no definida
        }fin
        '''
    },
    {
        "name": "Test String Concatenation",
        "description": "Realiza operaciones de concatenación entre cadenas y verifica que se manejen correctamente.",
        "code": '''
        programa TestStringConcatenation;
        vars
            greeting: cadena;
            name: cadena;

        inicio{
            greeting = "Hola, ";
            name = "Mundo!";
            escribe(greeting + name); // Concatenación de cadenas
        }fin
        '''
    },
    {
        "name": "Test Function Depth",
        "description": "Crea múltiples niveles de funciones anidadas para verificar que la pila de contextos se gestione correctamente sin desbordamientos.",
        "code": '''
        programa TestFunctionDepth;
        vars
            result: entero;

        nula level1() {
            nula level2() {
                nula level3() {
                    result = 30;
                    escribe("Resultado en level3: ", result);
                };
                level3();
            };
            level2();
        };

        inicio{
            level1();
            escribe("Resultado final: ", result);
        }fin
        '''
    },
    {
        "name": "Test Many Temporaries",
        "description": "Crea un programa que utilice una gran cantidad de variables temporales para verificar que la máquina virtual maneje adecuadamente la memoria y los temporales sin colapsar.",
        "code": '''
        programa TestManyTemporaries;
        vars
            a: entero;

        nula compute() {
            vars
                temp1, temp2, temp3, temp4, temp5: entero;
            {
                temp1 = 1;
                temp2 = 2;
                temp3 = 3;
                temp4 = 4;
                temp5 = 5;
                a = temp1 + temp2 + temp3 + temp4 + temp5;
                escribe("Suma total: ", a);
            }
        };

        inicio{
            compute();
        }fin
        '''
    },
    {
        "name": "Test Integration",
        "description": "Combina múltiples aspectos del lenguaje en un solo programa para verificar la integración correcta de todas las funcionalidades.",
        "code": '''
        programa TestIntegration;
        vars
            a, b: entero;
            msg: cadena;

        nula multiply(x: entero, y: entero) {
            vars
                product: entero;
            {
                product = x * y;
                escribe("Producto: ", product);
            }
        };

        nula mainFunction(z: entero) {
            vars
                sum: entero;
            {
                sum = z + 10;
                escribe("Suma: ", sum);
                multiply(sum, z);
            }
        };

        inicio{
            a = 5;
            b = 3;
            msg = "Inicio del programa.";
            escribe(msg);
            mainFunction(a);
            mientras (a < 20) haz {
                escribe("a: ", a);
                a = a + b;
            };
        }fin
        '''
    },
]


def run_test_case(test_case):
    """
    Ejecuta un caso de prueba dado.
    """
    print(f"\n=== Ejecutando Test: {test_case['name']} ===")
    print(f"Descripción: {test_case['description']}\n")
    programa = test_case["code"]

    try:
        # Preparar el input para ANTLR
        input_stream = InputStream(programa)
        lexer = PequePatitoLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = PequePatitoParser(stream)

        # Verificar si hay errores de sintaxis
        if parser.getNumberOfSyntaxErrors() > 0:
            print("Error: Se encontraron errores de sintaxis en el archivo.")
            return

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
            return
        else:
            print("Análisis semántico completado sin errores.\n")

        # Imprimir la tabla de variables y el directorio de funciones
        print("--- Tablas de Variables ---")
        tabla_variables.imprimir_tabla()
        print("\n--- Directorio de Funciones ---")
        directorio_funciones.imprimir_directorio()

        # Imprimir la tabla de constantes
        print("\n--- Tabla de Constantes ---")
        listener.tabla_constantes.imprimir_constantes()

        # Imprimir la fila de cuadruplos
        print("\n--- Cuádruplos Generados ---")
        listener.fila_cuadruplos.imprimir_cuadruplos()

        # Ejecutar la máquina virtual
        print("\n--- Ejecución de la Máquina Virtual ---")
        vm = MaquinaVirtual(listener.fila_cuadruplos.cuadruplos, listener.tabla_constantes, tabla_variables,
                            directorio_funciones)
        vm.ejecutar()

    except Exception as e:
        print(f"Error durante la ejecución del test '{test_case['name']}': {e}")
        traceback.print_exc()


def main():
    """
    Ejecuta todos los casos de prueba.
    """
    for test_case in test_cases:
        run_test_case(test_case)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
