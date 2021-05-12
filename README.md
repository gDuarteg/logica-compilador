# logica-compilador

## EBNF

BLOCK = "{", { COMMAND }, "}" ; 

COMMAND = ( λ | ASSIGNMENT | PRINT | BLOCK | WHILE | IF), ";" ; 

WHILE = "while", "(", OREXPR ,")", COMMAND;

IF = "if", "(", OREXPR ,")", COMMAND, (("else", COMMAND) | λ );

ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ; 

PRINT = "println", "(", OREXPR, ")" ; 

OREXPR = ANDEXPR, { "||", ANDEXPR } ;

ANDEXPR = EQEXPR, { "&&", EQEXPR } ;

EQEXPR = RELEXPR, { "==", RELEXPR } ;

RELEXPR = EXPRESSION, { (">"|"<"),  EXPRESSION }

EXPRESSION = TERM, { ("+" | "-"), TERM } ; 

TERM = FACTOR, { ("*" | "/"), FACTOR } ; 

FACTOR = (("+" | "-" | "!" ), FACTOR) | NUMBER | "(", OREXPR,  ")" | IDENTIFIER | READLN;

READLN = "readln", "(",")";

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ; 

NUMBER = DIGIT, { DIGIT } ; 

LETTER = ( a | ... | z | A | ... | Z ) ; 

DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;


## Diagrama Sintático

![alt text](https://github.com/gDuarteg/logica-compilador/blob/main/ds.png)
