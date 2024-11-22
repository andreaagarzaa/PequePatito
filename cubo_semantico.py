# cubo_semantico.py
class CuboSemantico:
    """
    Clase que representa el cubo semántico utilizado en la verificación de tipos en un compilador.
    """
    def __init__(self):
        # Estructura de cubo semántico para PequePatito organizada por operadores y tipos en un diccionario
        self.cubo = {
            # Operadores Aritméticos
            '+': {
                'entero': {'entero': 'entero', 'flotante': 'flotante'},
                'flotante': {'entero': 'flotante', 'flotante': 'flotante'},
                'booleano': {'booleano': 'error'}
            },
            '-': {
                'entero': {'entero': 'entero', 'flotante': 'flotante'},
                'flotante': {'entero': 'flotante', 'flotante': 'flotante'},
                'booleano': {'booleano': 'error'}
            },
            '*': {
                'entero': {'entero': 'entero', 'flotante': 'flotante'},
                'flotante': {'entero': 'flotante', 'flotante': 'flotante'},
                'booleano': {'booleano': 'error'}
            },
            '/': {
                'entero': {'entero': 'flotante', 'flotante': 'flotante'},
                'flotante': {'entero': 'flotante', 'flotante': 'flotante'},
                'booleano': {'booleano': 'error'}
            },
            # Operadores Relacionales
            '>': {
                'entero': {'entero': 'booleano', 'flotante': 'booleano'},
                'flotante': {'entero': 'booleano', 'flotante': 'booleano'}
            },
            '<': {
                'entero': {'entero': 'booleano', 'flotante': 'booleano'},
                'flotante': {'entero': 'booleano', 'flotante': 'booleano'}
            },
            '==': {
                'entero': {'entero': 'booleano', 'flotante': 'booleano'},
                'flotante': {'entero': 'booleano', 'flotante': 'booleano'},
                'booleano': {'booleano': 'booleano'}
            },
            '!=': {
                'entero': {'entero': 'booleano', 'flotante': 'booleano'},
                'flotante': {'entero': 'booleano', 'flotante': 'booleano'},
                'booleano': {'booleano': 'booleano'}
            },
            # Operadores Lógicos
            '&&': {
                'booleano': {'booleano': 'booleano'}
            },
            '||': {
                'booleano': {'booleano': 'booleano'}
            },
            '!': {
                'booleano': {'': 'booleano'}
            },
            # Operador de Asignación
            '=': {
                'entero': {'entero': 'entero', 'flotante': 'error', 'booleano': 'error'},  # No se permite asignación de flotante o booleano a entero
                'flotante': {'entero': 'error', 'flotante': 'flotante', 'booleano': 'error'},
                'booleano': {'entero': 'error', 'flotante': 'error', 'booleano': 'booleano'}
            }
        }

    def obtener_tipo(self, tipo_izq, tipo_der, operador):
        """
        Devuelve el tipo resultante de aplicar el operador especificado a los operandos dados.

        Args:
            tipo_izq (str): El tipo del operando izquierdo.
            tipo_der (str): El tipo del operando derecho. Para operadores unarios, puede ser None.
            operador (str): El operador a aplicar.

        Returns:
            str: El tipo resultante de aplicar el operador a los operandos, o 'error' si no es posible.
        """
        # Verificamos que el operador y los tipos izquierdo y derecho existan en el cubo
        if operador in self.cubo:
            if tipo_izq in self.cubo[operador]:
                if tipo_der is not None:
                    return self.cubo[operador][tipo_izq].get(tipo_der, 'error')
                else:
                    # Para operadores unarios como '!'
                    return self.cubo[operador][tipo_izq].get('', 'error')
        return 'error'

# Ejemplo de prueba
if __name__ == "__main__":
    cubo_semantico = CuboSemantico()

    # Pruebas para la suma
    print("entero + entero =", cubo_semantico.obtener_tipo('entero', 'entero', '+'))  # Debería retornar 'entero'
    print("entero + flotante =", cubo_semantico.obtener_tipo('entero', 'flotante', '+'))  # Debería retornar 'flotante'
    print("flotante + flotante =", cubo_semantico.obtener_tipo('flotante', 'flotante', '+'))  # Debería retornar 'flotante'

    # Pruebas para la comparación
    print("entero > flotante =", cubo_semantico.obtener_tipo('entero', 'flotante', '>'))  # Debería retornar 'booleano'

    # Pruebas para la asignación
    print("entero = flotante =", cubo_semantico.obtener_tipo('entero', 'flotante', '='))  # Debería retornar 'error'
    print("flotante = entero =", cubo_semantico.obtener_tipo('flotante', 'entero', '='))  # Debería retornar 'error'