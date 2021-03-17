# logica-compilador

## EBNF

EXPRESSION = TERM, { ("+" | "-"), TERM } ;

TERM = FACTOR, { ("*" | "/"), FACTOR } ;

FACTOR = ("+" | "-"), FACTOR | "(", EXPRESSION,")" | number ;


## Diagrama Sintático

![alt text](https://github.com/gDuarteg/logica-compilador/blob/main/ds.png)
