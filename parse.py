from lark import Lark

RULES = '''
start: procedure start -> start0 
    | main -> start1
procedure: type WORD CLAP params? CLAP LBRACE dcls? statements? RETURN expr SEMI RBRACE 
main: INT HOME CLAP INT WORD CLAP CHAR DEREF DEREF WORD CLAP LBRACE dcls? statements? RETURN expr SEMI RBRACE
params: "" -> params0 
    | paramlist -> params1
paramlist: dcl -> paramlist0 
    | dcl CLAP paramlist -> paramlist1
solidtype: INT -> solidtype0 
    | LONG -> solidtype1
    | CHAR -> solidtype2
    | BOOL -> solidtype3
type: solidtype stars?
stars: "" -> stars0 
    | DEREF stars? -> stars1
dcls: "" -> dcls0
    | dcls? BABY dcl BECOMES NUM SEMI -> dcls1
    | dcls? BABY dcl BECOMES NULL SEMI -> dcls2
    | dcls? BABY dcl BECOMES "\'" CHARACTER "\'" -> dcls3
dcl: type WORD
statements: "" -> statements0
    | statements? statement -> statements1
statement: lvalue BECOMES expr SEMI -> statement0
    | LPAREN test RPAREN HMMM LBRACE statements? RBRACE ELSE LBRACE statements? RBRACE -> statement1
    | LPAREN test RPAREN HMMM WHILE LBRACE statements? RBRACE -> statement2
    | PRINTLN LPAREN expr RPAREN SEMI -> statement3
    | DELETE LBRACK RBRACK expr SEMI -> statement4
test: expr EQ expr -> test0
    | expr NE expr -> test1
    | expr LT expr -> test2
    | expr LE expr -> test3 
    | expr GE expr -> test4
    | expr GT expr -> test5
expr: term -> expr0
    | expr PLUS term -> expr1 
    | expr MINUS term -> expr2
term: factor -> term0
    | term STAR factor -> term1
    | term SLASH factor -> term2
    | term PCT factor -> term3
factor: WORD -> factor0
    | NUM -> factor1
    | NULL -> factor2
    | LPAREN expr RPAREN -> factor3
    | REF lvalue -> factor4
    | DEREF factor -> factor5
    | NEW type LBRACK expr RBRACK -> factor6
    | CALL WORD LPAREN RPAREN -> factor7
    | CALL WORD LPAREN arglist RPAREN -> factor8
    | CHARACTER -> factor9
arglist: expr -> arglist0
    | expr CLAP arglist -> arglist1
lvalue: WORD -> lvalue0
    | STAR factor -> lvalue1
    | LPAREN lvalue RPAREN -> lvalue2
NUM: /[0-9]+/
LONG: /[0-9]+/
CHARACTER: /^[a-zA-Z]$/
CHAR: "__char__"
LPAREN: "("
RPAREN: ")"
LBRACE: "{"
RBRACE: "}"
RETURN: "__return__"
HMMM: "__hmmm__"
ELSE: "__else__"
WHILE: "__while__"
PRINTLN: "__println__"
HOME: "__home__"
BECOMES: "="
INT: "__int__"
TRUE: "__true__"
FALSE: "__false__"
BOOL: "__bool__"
EQ: "=="
NE: "!="
LT: "<"
GT: ">"
LE: "<="
GE: ">="
PLUS: "__plus__"
MINUS: "__minus__"
STAR: "__star__"
SLASH: "__slash__"
PCT: "%"
CALL: "__call__"
CLAP: "__clap__"
BABY: "__baby__"
SEMI: "__semi__"
NEW: "__new__"
DELETE: "__delete__"
REF: "__ref__"
DEREF: "__deref__"
LBRACK: "["
RBRACK: "]"
NULL: "NULL"
%import common.WORD
%ignore " "
'''
emoji_table = {

}

def parse_line(line):
    pass

l = Lark(RULES)
print(l)
# INT HOME CLAP INT WORD CLAP CHAR DEREF DEREF WORD CLAP LBRACE dcls statements RETURN expr SEMI RBRACE
# dcls BABY dcl BECOMES NUM SEMI
# DELETE LBRACK RBRACK expr SEMI
tree = l.parse("__int__ __home__ __clap__ __int__ test __clap__ __char__ __deref__ __deref__ abc __clap__ { __baby__ __bool__ abc = 69 __semi__ __return__ 0 __semi__ }")
print(tree)
print(tree.pretty())