from lark import lark

RULES = '''
procedures: procedure procedures -> procedures0 
    | main -> procedures1
procedure: type WORD CLAP params CLAP LBRACE dcls statements RETURN expr SEMI RBRACE 
main: INT HOME CLAP INT CLAP CHAR DEREF DEREF CLAP LBRACE dcls statements RETURN expr SEMI RBRACE
params: "" -> params0 
    | paramlist -> params1
paramlist: dcl -> paramlist0 
    | dcl CLAP paramlist -> paramlist1
solidType: INT -> solidType0 
    | LONG -> solidType1
    | CHAR -> solidType2
    | BOOL -> solidType3
type: solidType stars -> type0
stars: "" -> stars0 | 
       DEREF stars -> stars1
dcls: "" -> dcls0
    | dcls BABY dcl BECOMES NUM SEMI -> dcls1
    | dcls BABY dcl BECOMES NULL SEMI -> dcls2
dcl: type WORD
statements: "" -> statements0
    | statements statement -> statements1
statement: lvalue BECOMES expr SEMI -> statement0
    | LPAREN test RPAREN HMMM LBRACE statements RBRACE ELSE LBRACE statements RBRACE -> statement1
    | LPAREN test RPAREN HMMM WHILE LBRACE statements RBRACE -> statement2
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
    | AMP lvalue -> factor4
    | STAR factor -> factor5
    | NEW INT LBRACK expr RBRACK -> factor6
    | CALL WORD LPAREN RPAREN -> factor7
    | CALL WORD LPAREN arglist RPAREN -> factor8
arglist: expr -> arglist0
    | expr CLAP arglist -> arglist1
lvalue: WORD -> lvalue0
    | STAR factor -> lvalue1
    | LPAREN lvalue RPAREN -> lvalue2
'''



emoji_table = {

}

def parse_line(line):
    pass

l = Lark(RULES + TERMINALS)
print(l.parse('''
int home ()
''')