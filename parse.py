from lark import Lark
import sys
import convert_code

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
    | dcls? BABY dcl BECOMES "'" CHARACTER "'" SEMI -> dcls3
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
    | CALL WORD CLAP CLAP -> factor7
    | CALL WORD CLAP arglist CLAP -> factor8
    | "'" CHARACTER "'" -> factor9
arglist: expr -> arglist0
    | expr CLAP arglist -> arglist1
lvalue: WORD -> lvalue0
    | STAR factor -> lvalue1
    | LPAREN lvalue RPAREN -> lvalue2
NUM: /[0-9]+/
LONG: /[0-9]+/
CHARACTER: /[a-zA-Z]/
CHAR: "_char_"
LPAREN: "("
RPAREN: ")"
LBRACE: "{"
RBRACE: "}"
RETURN: "_return_"
HMMM: "_hmmm_"
ELSE: "_else_"
WHILE: "_while_"
PRINTLN: "_println_"
HOME: "_home_"
BECOMES: "="
INT: "_int_"
TRUE: "_true_"
FALSE: "_false_"
BOOL: "_bool_"
EQ: "=="
NE: "!="
LT: "<"
GT: ">"
LE: "<="
GE: ">="
PLUS: "_plus_"
MINUS: "_minus_"
STAR: "_star_"
SLASH: "_slash_"
PCT: "%"
CALL: "_call_"
CLAP: "_clap_"
BABY: "_baby_"
SEMI: "_semi_"
NEW: "_new_"
DELETE: "_delete_"
REF: "_ref_"
DEREF: "_deref_"
LBRACK: "["
RBRACK: "]"
NULL: "NULL"
%import common.WORD
%ignore " "
'''



# emoji unicode to 
emoji_table = {
    u'\U0001f170': '__char__',
    u'\U0001F51A': '__return__',
    u'\U0001F914': '__hmmm__',
    u'\U0001F937': '__else__',
    u'\U000023F1': '__while__',
    u'\U0001F5A8': '__println__',
    u'\U0001F3E0': '__home__', 
    u'\U0001F4AF': '__int__', 
    u'\U0001f44d': '__true__', 
    u'\U0001f44e': '__false__', 
    u'\U0001f171': '__bool__',
    u'\U00002795': '__plus__', 
    u'\U00002796': '__minus__', 
    u'\U00002716': '__star__', 
    u'\U00002797':'__slash__', 
    u'\U0001f4f2': '__call__', 
    u'\U0001f44f': '__clap__', 
    u'\U0001f476': '__baby__', 
    u'\U0001f44c': '__semi__', 
    u'\U0001f195': '__new__', 
    u'\U0001f5d1': '__delete__', 
    u'\U0001f448': '__ref__', 
    u'\U0001f449': '__deref__'
}

# Returns a parse-tree from a Cmoji file
def parse_file(file_name):
    larker = Lark(RULES)
    parse_string = ''
    with open(file_name, 'r', ) as f:
        for line in f.read().split('\n'):
            parse_string += line

    # Pre-processes the cmoji file, replacing emojis with their parse equivelants
    for emoji in emoji_table:
        parse_string = parse_string.replace(emoji, emoji_table[emoji])

    parse_string = parse_string.replace('\t', ' ').replace('\n', ' ')
    try:
        tree = larker.parse(parse_string)
    except Exception:
        print(parse_string)
        print('Needs more emoji\'s, mate')
        raise Exception
        
    return tree

if len(sys.argv) > 1:
    convert_code.convert(parse_file(sys.argv[1]))
