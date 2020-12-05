/**
 * Student Name: Bùi Đức Huy, Student ID: 1812336
 */
grammar BKIT;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    result = super().emit()
    if tk == self.UNCLOSE_STRING:       
        raise UncloseString(result.text)
    elif tk == self.ILLEGAL_ESCAPE:
        raise IllegalEscape(result.text)
    elif tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)
    elif tk == self.UNTERMINATED_COMMENT:
        raise UnterminatedComment()
    else:
        return result;
}

options {
	language = Python3;
}

program: many_declare EOF;

many_declare: var_declare_list? func_declare_list?;

var_declare_list: var_declare var_declare_list | var_declare;

func_declare_list:
	func_declare func_declare_list
	| func_declare;

// VARIABLE DECLARE
var_declare: VAR COLON ids_list SEMI;

ids_list: id_declare (COMMA ids_list) | id_declare;

id_declare: ID (array_declares)? (ASSIGN type_list)?;

array_declares: array (array_declares) | array;

array: (LSB INTLIT RSB);

array_id: (ID | function_call) list_index;

type_list:
	INTLIT
	| FLOATLIT
	| TRUE
	| FALSE
	| STRINGLIT
	| array_lit;

// FUNCTION DECLARE
func_declare: header_stm (paramater_stm)? body_stm;

header_stm: FUNCTION COLON ID;
paramater_stm: PARAMETER COLON paramater_list;
paramater_list: ids_list (COMMA paramater_list) | ids_list;
body_stm:
	BODY COLON var_declare_list? statement_list? ENDBODY DOT;
statement_list: statement statement_list | statement;

statement:
	assign_statement
	| if_statement
	| for_statement
	| while_statement
	| do_while_statement
	| break_statement
	| continue_statement
	| function_call_statement
	| return_statement;

assign_statement: (ID | array_id) ASSIGN expressions SEMI;

// IF STATEMENT
if_statement:
	if_then_statement (else_if_statements)? (else_statement)? ENDIF DOT;
if_then_statement:
	IF expressions THEN var_declare_list? statement_list?;
else_if_statements:
	else_if_statement else_if_statements
	| else_if_statement;
else_if_statement:
	ELSEIF expressions THEN var_declare_list? statement_list?;
else_statement: ELSE var_declare_list? statement_list?;

// FOR STATEMENT
for_statement:
	FOR LB for_condition RB DO var_declare_list? statement_list? ENDFOR DOT;
for_condition: (ID ASSIGN expressions) COMMA expressions COMMA (
		(ID ASSIGN expressions)
		| expressions
	);

// WHILE STATEMENT
while_statement:
	WHILE expressions DO var_declare_list? statement_list? ENDWHILE DOT;

// DO WHILE STATEMENT
do_while_statement:
	DO var_declare_list? statement_list? WHILE expressions ENDDO DOT;

// BREAK STATEMENT
break_statement: BREAK SEMI;

// CONTINUE STATEMENT
continue_statement: CONTINUE SEMI;

// FUNCTION CALL STATEMENT
function_call_statement:
	ID LB expressions? (COMMA expressions)* RB SEMI;

// RETUNR STATEMENT
return_statement: RETURN expressions? SEMI;

expressions:
	exp1 EQUALOP exp1
	| exp1 NOTEQUALOP exp1
	| exp1 LESSOP exp1
	| exp1 LESSOREQUALOP exp1
	| exp1 GREATEROP exp1
	| exp1 GREATEOREQUALOP exp1
	| exp1 NOTEQUALOPFLOAT exp1
	| exp1 LESSOPDOT exp1
	| exp1 LESSOREQUALOPDOT exp1
	| exp1 GREATEROPDOT exp1
	| exp1 GREATEOREQUALOPDOT exp1
	| exp1;
exp1: exp1 ANDOP exp2 | exp1 OROP exp2 | exp2;
exp2:
	exp2 ADDOP exp3
	| exp2 ADDOPDOT exp3
	| exp2 SUBOP exp3
	| exp2 SUBOPDOT exp3
	| exp3;
exp3:
	exp3 MULOP exp4
	| exp3 MULOPDOT exp4
	| exp3 DIVOP exp4
	| exp3 DIVOPDOT exp4
	| exp3 MODOP exp4
	| exp4;
exp4: NOTOP exp5 | exp5;
exp5: (SUBOP | SUBOPDOT) exp6 | exp6;
exp6: operand list_index | operand;
operand:
	type_list
	| ID
	| sub_expression
	| array_id
	| function_call
	| index_operator;
sub_expression: LB expressions RB;
function_call: ID LB list_expression? RB;
list_expression:
	expressions (COMMA list_expression)
	| expressions;
index_operator: ID list_index;
list_index: index list_index | index;
index: LSB list_expression RSB;
// IDENTIFIER
ID: [a-z][a-zA-Z0-9_]*;

// KEYWORD
BODY: 'Body';
BREAK: 'Break';
CONTINUE: 'Continue';
DO: 'Do';
ELSE: 'Else';
ELSEIF: 'ElseIf';
ENDBODY: 'EndBody';
ENDIF: 'EndIf';
ENDFOR: 'EndFor';
ENDWHILE: 'EndWhile';
FOR: 'For';
FUNCTION: 'Function';
IF: 'If';
PARAMETER: 'Parameter';
RETURN: 'Return';
THEN: 'Then';
VAR: 'Var';
WHILE: 'While';
TRUE: 'True';
FALSE: 'False';
ENDDO: 'EndDo';

// OPERATORS
ASSIGN: '=';

ADDOP: '+';
ADDOPDOT: '+.';

SUBOP: '-';
SUBOPDOT: '-.';

MULOP: '*';
MULOPDOT: '*.';

DIVOP: '\\';
DIVOPDOT: '\\.';

MODOP: '%';

NOTOP: '!';
OROP: '||';
ANDOP: '&&';

EQUALOP: '==';

NOTEQUALOP: '!=';
NOTEQUALOPFLOAT: '=/=';

LESSOP: '<';
LESSOPDOT: '<.';

GREATEROP: '>';
GREATEROPDOT: '>.';

LESSOREQUALOP: '<=';
LESSOREQUALOPDOT: '<=.';

GREATEOREQUALOP: '>=';
GREATEOREQUALOPDOT: '>=.';

// SEPARATOR
LB: '(';
RB: ')';

LSB: '[';
RSB: ']';

COLON: ':';
DOT: '.';
COMMA: ',';
SEMI: ';';

LP: '{';
RP: '}';

// LITERALS
INTLIT: DEC | HEX | OCT;
fragment DEC: [1-9][0-9]+ | [0-9];
fragment HEX: ([0][Xx][0-9]+) | ([0][Xx][A-F]+);
fragment OCT: [0][Oo][0-7]+;

FLOATLIT:
	Digit+ DOT Digit+ Expo?
	| Digit+ DOT? Expo
	| Digit+ DOT
	| DOT Digit+;

fragment Digit: [0-9];
fragment Expo: [eE] (SUBOP | ADDOP)? Digit+;

// fragment BOOLEAN: TRUE | FALSE;

// STRING
STRINGLIT:
	'"' STR_CHAR* '"' {
        self.text = self.text[1:-1];
    };
fragment STR_CHAR: STR_CHAR_NORMAL | STR_CHAR_QUOTE;
fragment STR_CHAR_NORMAL: ~[\b\t\n\f\r'"\\] | ESC_SEQ;
fragment ESC_SEQ: '\\' [btnfr'\\];
fragment STR_CHAR_QUOTE: '\'"';

fragment INTLIT_LIST: INTLIT (COMMA INTLIT)*;
fragment FLOATLIT_LIST: FLOATLIT (COMMA FLOATLIT)*;
fragment STRING_LIST: STRINGLIT ( COMMA STRINGLIT)*;
fragment BOOLEAN_LIST: (TRUE | FALSE) (COMMA (TRUE | FALSE))*;

array_lit: LP array_lits? RP;
array_lits: type_list COMMA array_lits | type_list;
// fail

WS: [ \t\r\n]+ -> skip;
COMMENT: '**' .*? '**' -> skip;
// skip spaces, tabs, newlines

ERROR_CHAR: .{raise ErrorToken(self.text)};
UNCLOSE_STRING:
	'"' (STR_CHAR)* {raise UncloseString(self.text[1:])};
ILLEGAL_ESCAPE:
	UNCLOSE_STRING '\\' ~([brnft] | '"' | '\\') { raise IllegalEscape(self.text[1:])};
UNTERMINATED_COMMENT: .;