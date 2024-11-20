# maquina_virtual.py
from memoria_ejecucion import MemoriaEjecucion

class MaquinaVirtual:
    def __init__(self, cuadruplos, tabla_constantes):
        self.cuadruplos = cuadruplos
        self.memoria = MemoriaEjecucion()
        self.tabla_constantes = tabla_constantes
        self.inicializar_constantes()

    def inicializar_constantes(self):
        # Cargar las constantes en la memoria de ejecución
        for valor, direccion in self.tabla_constantes.constantes.items():
            if valor.startswith('"') and valor.endswith('"'):
                # Es una cadena
                self.memoria.escribir(direccion, valor.strip('"'))
            elif '.' in valor:
                # Es un flotante
                self.memoria.escribir(direccion, float(valor))
            else:
                # Es un entero
                self.memoria.escribir(direccion, int(valor))

    def ejecutar(self):
        contador = 0
        while contador < len(self.cuadruplos):
            cuad = self.cuadruplos[contador]
            operador, op1, op2, res = cuad
            # Implementar cada caso según el operador
            if operador == '+':
                val1 = self.memoria.leer(op1)
                val2 = self.memoria.leer(op2)
                self.memoria.escribir(res, val1 + val2)
            elif operador == '-':
                val1 = self.memoria.leer(op1)
                val2 = self.memoria.leer(op2)
                self.memoria.escribir(res, val1 - val2)
            elif operador == '*':
                val1 = self.memoria.leer(op1)
                val2 = self.memoria.leer(op2)
                self.memoria.escribir(res, val1 * val2)
            elif operador == '/':
                val1 = self.memoria.leer(op1)
                val2 = self.memoria.leer(op2)
                if val2 == 0:
                    print("Error: División por cero.")
                    return
                self.memoria.escribir(res, val1 / val2)
            elif operador == '=':
                val = self.memoria.leer(op1)
                self.memoria.escribir(res, val)
            elif operador == 'print':
                val = self.memoria.leer(op1)
                print(val)
            elif operador == '>':
                val1 = self.memoria.leer(op1)
                val2 = self.memoria.leer(op2)
                self.memoria.escribir(res, val1 > val2)
            elif operador == '<':
                val1 = self.memoria.leer(op1)
                val2 = self.memoria.leer(op2)
                self.memoria.escribir(res, val1 < val2)
            elif operador == '==':
                val1 = self.memoria.leer(op1)
                val2 = self.memoria.leer(op2)
                self.memoria.escribir(res, val1 == val2)
            elif operador == '!=':
                val1 = self.memoria.leer(op1)
                val2 = self.memoria.leer(op2)
                self.memoria.escribir(res, val1 != val2)
            elif operador == 'GOTO':
                contador = res - 1  # Restamos 1 porque al final del loop se incrementa
            elif operador == 'GOTOF':
                val = self.memoria.leer(op1)
                if not val:
                    contador = res - 1
            elif operador == 'END':
                break
            else:
                print(f"Error: Operador desconocido '{operador}'.")
                return
            contador += 1
