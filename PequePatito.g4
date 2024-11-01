grammar PequePatito;

// Regla inicial del programa
programa : p v f INICIO cuerpo FIN;
p: PROGRAMA ID PUNTO_Y_COMA;
//v: vars;
v : VARS var_declaracion*;  // Declaración múltiple de variables

f: funcs*;

// Reglas de variables y funciones
vars : VARS var_declaracion*;

//vars : VARS var_declaracion | ;
//var_declaracion : ( id_list DOS_PUNTOS tipo PUNTO_Y_COMA) vars_list;
var_declaracion : id_list DOS_PUNTOS tipo PUNTO_Y_COMA;
id_list : ID (COMA ID)*;
vars_list: ( id_list DOS_PUNTOS tipo PUNTO_Y_COMA)*;

// Reglas de funciones
//funcs : NULA ID PARENTESIS_IZQ params PARENTESIS_DER LLAVE_IZQ vars? cuerpo LLAVE_DER PUNTO_Y_COMA ;
funcs : NULA ID PARENTESIS_IZQ params? PARENTESIS_DER LLAVE_IZQ vars? cuerpo LLAVE_DER PUNTO_Y_COMA;

params : (ID DOS_PUNTOS tipo (COMA ID DOS_PUNTOS tipo)*) |  ;


// Cuerpo del programa
cuerpo : LLAVE_IZQ estatutos LLAVE_DER;

// Reglas de sentencias
estatutos: estatuto*; // Permite cero o más estatutos
estatuto: asigna
          | condicion
          | ciclo
          | llamada
          | imprime;

asigna: ID ASIGNACION expresion PUNTO_Y_COMA; // Asignación
imprime: IMPRIME PARENTESIS_IZQ (p_imp) PARENTESIS_DER PUNTO_Y_COMA; // Imprime
p_imp : (expresion | LETRERO) (COMA p_imp)* ;// Imprime
condicion: SI PARENTESIS_IZQ expresion PARENTESIS_DER cuerpo else_part PUNTO_Y_COMA; // Condicional
else_part: SINO cuerpo | ; // Parte del else (opcional)
ciclo: MIETRAS PARENTESIS_IZQ expresion PARENTESIS_DER HAZ cuerpo PUNTO_Y_COMA; // Ciclo
llamada: ID PARENTESIS_IZQ (expresion (COMA expresion)*)? PARENTESIS_DER PUNTO_Y_COMA; // Llamada a función


// Expresiones y operadores
expresion : bo;
exp : termino ((SUMA | RESTA) termino)*  ;

termino:  factor ((MULTIPLICACION| DIVISION) factor)* ;

bo: exp (('>' | '<' | '==' | '!=') exp)?;

factor : PARENTESIS_IZQ expresion PARENTESIS_DER | f_otro;
f_otro: (SUMA | RESTA)?  (ID | cte);

// Tipos y literales
tipo : ENT | FLOT ;
cte : CTE_ENT | CTE_FLOT ;


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
IMPRIME: 'escribe';

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
IGUAL: '==';                     // Igual
DIFERENTE: '!=';                 // Diferente

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
CTE_ENT: [0-9]+;                 // Constantes enteras
CTE_FLOT: [0-9]+ '.' [0-9]+;     // Constantes flotantes
LETRERO: '"' ~["\r\n]* '"';        // Literales de cadena

// ---------------------------------------------------
// 5. Espacios en blanco
// ---------------------------------------------------
ID: [a-zA-Z_][a-zA-Z_0-9]*;     // Identificadores (nombres de variables y funciones)
WS: [ \t\r\n]+ -> skip;          // Espacios en blanco
