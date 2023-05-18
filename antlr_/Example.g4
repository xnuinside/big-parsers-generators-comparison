grammar Example;

start : line+ ;

line : key ':' value ;

key : ID ;

value : FLOAT
      | INT
      | DATE
      | DATE_RANGE;

expr : value op=( '&' | '-' ) value ;

FLOAT : DIGIT+ '.' DIGIT+ ;
INT : DIGIT+ ;
DATE : DIGIT{4} '-' DIGIT{2} '-' DIGIT{2} ;
DATE_RANGE : DATE '/' DATE ;

ID : [a-zA-Z_][a-zA-Z0-9_]* ;

WS : [ \t\r\n] -> skip ;

fragment DIGIT : [0-9] ;
