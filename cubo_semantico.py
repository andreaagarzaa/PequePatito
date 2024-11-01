# cubo_semantico.py
class CuboSemantico:
    """
    Clase que representa el cubo semántico utilizado en la verificación de tipos en un compilador.
    """

    def __init__(self):
        # Estructura de cubo semántico para PequePatito organizada por operadores y tipos en un diccionario anidado
        self.cubo = {
            '+': {
                'entero': {'entero': 'entero', 'flotante': 'flotante'},
                'flotante': {'entero': 'flotante', 'flotante': 'flotante'}
            },
            '-': {
                'entero': {'entero': 'entero', 'flotante': 'flotante'},
                'flotante': {'entero': 'flotante', 'flotante': 'flotante'}
            },
            '*': {
                'entero': {'entero': 'entero', 'flotante': 'flotante'},
                'flotante': {'entero': 'flotante', 'flotante': 'flotante'}
            },
            '/': {
                'entero': {'entero': 'flotante', 'flotante': 'flotante'},
                'flotante': {'entero': 'flotante', 'flotante': 'flotante'}
            },
            '>': {
                'entero': {'entero': 'bool', 'flotante': 'bool'},
                'flotante': {'entero': 'bool', 'flotante': 'bool'}
            },
            '<': {
                'entero': {'entero': 'bool', 'flotante': 'bool'},
                'flotante': {'entero': 'bool', 'flotante': 'bool'}
            },
            '==': {
                'entero': {'entero': 'bool', 'flotante': 'bool'},
                'flotante': {'entero': 'bool', 'flotante': 'bool'}
            },
            '!=': {
                'entero': {'entero': 'bool', 'flotante': 'bool'},
                'flotante': {'entero': 'bool', 'flotante': 'bool'}
            },
            '=': {
                'entero': {'entero': 'entero', 'flotante': 'error'},  # No se permite asignación de flotante a entero
                'flotante': {'entero': 'flotante', 'flotante': 'flotante'}
            }
        }

    def obtener_tipo(self, tipo_izq, tipo_der, operador):
        """
        Devuelve el tipo resultante de aplicar el operador especificado a los operandos dados.

        Args:
            tipo_izq (str): El tipo del operando izquierdo.
            tipo_der (str): El tipo del operando derecho.
            operador (str): El operador a aplicar.

        Returns:
            str: El tipo resultante de aplicar el operador a los operandos, o 'error' si no es posible.
        """
        # Verificamos que el operador y los tipos izquierdo y derecho existan en el cubo
        if operador in self.cubo:
            if tipo_izq in self.cubo[operador]:
                return self.cubo[operador][tipo_izq].get(tipo_der, 'error')
        return 'error'


# Ejemplo de prueba
if __name__ == "__main__":
    cubo_semantico = CuboSemantico()

    # Pruebas para la suma
    print("entero + entero =", cubo_semantico.obtener_tipo('entero', 'entero', '+'))  # Debería retornar 'entero'
    print("entero + flotante =", cubo_semantico.obtener_tipo('entero', 'flotante', '+'))  # Debería retornar 'flotante'
    print("flotante + flotante =", cubo_semantico.obtener_tipo('flotante', 'flotante', '+'))  # Debería retornar 'flotante'

    # Pruebas para la comparación
    print("entero > flotante =", cubo_semantico.obtener_tipo('entero', 'flotante', '>'))  # Debería retornar 'bool'

    # Pruebas para la asignación
    print("entero = flotante =", cubo_semantico.obtener_tipo('entero', 'flotante', '='))  # Debería retornar 'error'
    print("flotante = entero =", cubo_semantico.obtener_tipo('flotante', 'entero', '='))  # Debería retornar 'flotante'
