grammar PequePatito;

programa : p v f inicio cuerpo FIN;
inicio: INICIO;
p: PROGRAMA ID PUNTO_Y_COMA;
v : VARS var_declaracion*;
f: funcs*;

// Reglas de variables y funciones
vars : VARS var_declaracion*;
var_declaracion : id_list DOS_PUNTOS tipo PUNTO_Y_COMA;
id_list : ID (COMA ID)*;

funcs : NULA ID PARENTESIS_IZQ params? PARENTESIS_DER LLAVE_IZQ vars? cuerpo LLAVE_DER PUNTO_Y_COMA;

params : (ID DOS_PUNTOS tipo (COMA ID DOS_PUNTOS tipo)*)?;

// Cuerpo del programa
cuerpo : LLAVE_IZQ estatutos LLAVE_DER;

// Reglas de sentencias
estatutos: estatuto*; // Permite cero o más estatutos
estatuto: asigna
         | condicion
         | ciclo
         | llamada
         | imprime;

// Definiciones de sentencias individuales
asigna: ID ASIGNACION expresion PUNTO_Y_COMA; // Asignación
imprime: IMPRIME PARENTESIS_IZQ p_imp (COMA p_imp)* PARENTESIS_DER PUNTO_Y_COMA; // Impresión
//p_imp : (expresion | LETRERO ) (COMA (expresion | LETRERO))* ;
p_imp : expresion | LETRERO ; // se agrega a una lista de impresion
condicion: SI PARENTESIS_IZQ expresion PARENTESIS_DER cuerpo else_part PUNTO_Y_COMA; // Condicional
else_part: SINO cuerpo | ;
ciclo: MIETRAS PARENTESIS_IZQ expresion PARENTESIS_DER HAZ cuerpo PUNTO_Y_COMA; // Ciclo
// haz_ciclo: HAZ cuerpo MIETRAS PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_Y_COMA; // Ciclo
llamada: ID PARENTESIS_IZQ (expresion (COMA expresion)*)? PARENTESIS_DER PUNTO_Y_COMA; // Llamada a función
 expresion: exp (bo exp)?;
bo: MAYOR | MENOR | MAYOR_IGUAL | MENOR_IGUAL | DIFERENTE | IGUAL_IGUAL;

exp : termino (operador termino)*  ;
operador : SUMA | RESTA;
termino:  factor (operador_factor factor)* ;
operador_factor : MULTIPLICACION | DIVISION;
factor : PARENTESIS_IZQ expresion PARENTESIS_DER | (SUMA | RESTA) cte |  ID | NUMERO;

// Tipos y literales
tipo : ENT | FLOT;
cte : CTE_ENT | CTE_FLOT | NUMERO;

// ---------------------------------------------------
// 1. Palabras clave del lenguaje
// ---------------------------------------------------
PROGRAMA: 'programa';
INICIO: 'inicio';
FIN: 'fin';
VARS: 'vars';
SI: 'si';
SINO: 'sino';
MIETRAS: 'mientras';
HAZ: 'haz';
NULA: 'nula';

// ---------------------------------------------------
// 2. Tipos de datos
// ---------------------------------------------------
ENT: 'entero';
FLOT: 'flotante';
BOOL: 'booleano';
IMPRIME: 'escribe';
VERDADERO: 'verdadero';
FALSO: 'falso';

// ---------------------------------------------------
// 3. Operadores y delimitadores
// ---------------------------------------------------
// Operadores Aritméticos
SUMA: '+';                       // Suma
RESTA: '-';                      // Resta
MULTIPLICACION: '*';            // Multiplicación
DIVISION: '/';                   // División


// Operadores de Comparación
MAYOR: '>';                     // Mayor que
MENOR: '<';                      // Menor que
MAYOR_IGUAL: '>=';               // Mayor o igual
MENOR_IGUAL: '<=';               // Menor o igual
IGUAL_IGUAL: '==';               // Igual
//IGUAL: '==';                     // Igual
DIFERENTE: '!=';                 // Diferente

// Operadores Lógicos
AND: '&&';                       // AND
OR: '||';                        // OR
NOT: '!';                        // NOT

// Delimitadores
PARENTESIS_IZQ: '(';            // Paréntesis izquierdo
PARENTESIS_DER: ')';            // Paréntesis derecho
LLAVE_IZQ: '{';                 // Llave izquierda
LLAVE_DER: '}';                 // Llave derecha
PUNTO_Y_COMA: ';';              // Punto y coma
COMA: ',';                       // Coma
DOS_PUNTOS: ':';                 // Dos puntos
ASIGNACION: '=';                 // Asignación
BRACKET_IZQ: '[';                // Corchete izquierdo
BRACKET_DER: ']';                // Corchete derecho

// ---------------------------------------------------
// 4. Identificadores y Literales
// ---------------------------------------------------
CTE_ENT: 'cte_ent';                 // Constantes enteras
CTE_FLOT: 'cte_float';     // Constantes flotantes
NUMERO: [0-9]+ ('.' [0-9]+)?;
LETRERO: '"' ~["\r\n]* '"';      // Literales de cadena

// ---------------------------------------------------
// 5. Espacios en blanco
// ---------------------------------------------------
ID: [a-zA-Z_][a-zA-Z_0-9]*;     // Identificadores (nombres de variables y funciones)
WS: [ \t\r\n]+ -> skip;          // Espacios en blanco

// ---------------------------------------------------
// 6. Comentarios
// ---------------------------------------------------
LINE_COMMENT: '//' ~[\r\n]* -> skip;