import lark

def safe_convert(convert_fn, children, index, name, *args):
	if (index >= len(children)):
		return

	if type(children[index]) is lark.tree.Tree:
		if children[index].data == name:
			convert_fn(children[index], *args)

def get_type_from_emoji(emoji):
	emoji_dict = {
		"__int__": "int",
		"__bool__": "bool",
		"__char__": "char",
		"__deref__": "*",
		"__true__": "true",
		"__false__": "false"
	}

	if emoji in emoji_dict:
		return emoji_dict[emoji]

	return emoji

def concatenate_leaves(tree):
	s = ""

	stack = [tree]
	while len(stack) > 0:
		top = stack.pop()

		if type(top) is lark.lexer.Token:
			s += get_type_from_emoji(top.value)
		else:
			stack += top.children[::-1]

	return s



def convert_test(tree):
	convert_expr(tree.children[0])
	if tree.data == 'test0':
		print(" == ", end="")
	elif tree.data == 'test1':
		print(" != ", end="")
	elif tree.data == 'test2':
		print(" < ", end="")
	elif tree.data == 'test3':
		print(" <= ", end="")
	elif tree.data == 'test4':
		print(" >= ", end="")
	elif tree.data == 'test5':
		print(" > ", end="")

	convert_expr(tree.children[2])

def convert_type(tree):
	type = (concatenate_leaves(tree.children[0]))
	print(type, end="")
	if len(tree.children) > 1:
		print(concatenate_leaves(tree.children[1]), end="")

def convert_dcl(tree, indent):
	print(indent, end="")
	convert_type(tree.children[0])
	name = concatenate_leaves(tree.children[1])
	print(" " + name, end="")

def convert_dcls(tree, indent):
	if tree.data == 'dcls1':
		if type(tree.children[0]) is lark.tree.Tree and tree.children[0].data[:4] == 'dcls':
			convert_dcls(tree.children[0], indent)
			convert_dcl(tree.children[2], indent)
			print(" = %s;" % concatenate_leaves(tree.children[4]))
		else:
			convert_dcl(tree.children[1], indent)
			print(" = %s;" % concatenate_leaves(tree.children[3]))
	elif tree.data == 'dcls2':
		if type(tree.children[0]) is lark.tree.Tree and tree.children[0].data[:4] == 'dcls':
			convert_dcls(tree.children[0], indent)
			convert_dcl(tree.children[2], indent)
		else:
			convert_dcl(tree.children[1], indent)
		print(" = NULL;")
	elif tree.data == 'dcls3':
		if type(tree.children[0]) is lark.tree.Tree and tree.children[0].data[:4] == 'dcls':
			convert_dcls(tree.children[0], indent)
			convert_dcl(tree.children[2], indent)
			print(" = '%s';" % concatenate_leaves(tree.children[4]))
		else:
			convert_dcl(tree.children[1], indent)
			print(" = '%s';" % concatenate_leaves(tree.children[3]))

def convert_paramlist(tree):
	if tree.data == "paramlist0":
		convert_dcl(tree.children[0], "")
	elif tree.data == 'paramlist1':
		convert_dcl(tree.children[0], "")
		convert_paramlist(tree.children[2])

def convert_params(tree):
	if tree.data == 'params1':
		convert_paramlist(tree.children[0])

def convert_lvalue(tree, indent):
	if tree.data == 'lvalue0':
		print(indent + concatenate_leaves(tree.children[0]), end="")
	elif tree.data == 'lvalue1':
		print(indent + "*", end="")
		convert_factor(tree.children[1])
	elif tree.data == 'lvalue2':
		print(indent + "(", end="")
		convert_lvalue(tree.children[1], indent)
		print(")", end="")

def convert_arglist(tree):
	if tree.data == 'arglist0':
		convert_expr(tree.children[0])
	elif tree.data == 'arglist1':
		convert_expr(tree.children[0])
		print(", ", end="")
		convert_arglist(tree.children[2])

def convert_factor(tree):
	if tree.data == 'factor0' or tree.data == 'factor1':
		print(concatenate_leaves(tree.children[0]), end="")
	elif tree.data == 'factor2':
		print("NULL", end="")
	elif tree.data == 'factor3':
		print("(", end="")
		convert_expr(tree.children[1])
		print(")", end="")
	elif tree.data == 'factor4':
		print("&", end="")
		convert_lvalue(tree.children[1], "")
	elif tree.data == 'factor5':
		print("*", end="")
		convert_factor(tree.children[1])
	elif tree.data == 'factor6':
		print("new ", end="")
		convert_type(tree.children[1])
		print("[", end="")
		convert_expr(tree.children[3])
		print("]", end="")
	elif tree.data == 'factor7':
		fn_name = concatenate_leaves(tree.children[1])
		print(fn_name+"()", end="")
	elif tree.data == 'factor8':
		fn_name = concatenate_leaves(tree.children[1])
		print(fn_name+"(", end="")
		convert_arglist(tree.children[3])
		print(")", end="")


def convert_term(tree):
	if tree.data == 'term0':
		convert_factor(tree.children[0])
	elif tree.data == 'term1':
		convert_term(tree.children[0])
		print(" * ", end="")
		convert_factor(tree.children[2])
	elif tree.data == 'term2':
		convert_term(tree.children[0])
		print(" / ", end="")
		convert_factor(tree.children[2])
	elif tree.data == 'term3':
		convert_term(tree.children[0])
		print(" % ", end="")
		convert_factor(tree.children[2])

def convert_expr(tree):
	if tree.data == 'expr0':
		convert_term(tree.children[0])
	elif tree.data == 'expr1':
		convert_expr(tree.children[0])
		print(" + ", end="")
		convert_term(tree.children[2])
	elif tree.data == 'expr2':
		convert_expr(tree.children[0])
		print(" - ", end="")
		convert_term(tree.children[2])

def convert_statement(tree, indent):
	if tree.data == 'statement0':
		convert_lvalue(tree.children[0], indent)
		print(" = ", end="")
		convert_expr(tree.children[2])
		print(";")
	elif tree.data == 'statement1':
		print(indent + "if (", end="")
		convert_test(tree.children[1])
		print(") {")
		if type(tree.children[5]) is lark.tree.Tree and tree.children[5].data[:10] == 'statements':
			convert_statements(tree.children[5], indent+'\t')
		print(indent + "}")
		print(indent + "else {")
		if len(tree.children) > 9 and type(tree.children[9]) is lark.tree.Tree and tree.children[9].data[:10] == 'statements':
			convert_statements(tree.children[9], indent+'\t')
		elif type(tree.children[8]) is lark.tree.Tree and tree.children[8].data[:10] == 'statements':
			convert_statements(tree.children[8], indent+'\t')
		print(indent + "}")

	elif tree.data == 'statement2':
		print(indent+"while (", end="")
		convert_test(tree.children[1])
		print(") {")
		if type(tree.children[6]) is lark.tree.Tree and tree.children[6].data[:10] == 'statements':
			convert_statements(tree.children[6], indent+'\t')
		print(indent+"}")
	elif tree.data == 'statement3':
		print(indent + "cout << ", end="")
		convert_expr(tree.children[2])
		print(" << endl;")
	elif tree.data == 'statement4':
		print(indent + "delete[] ", end="")
		convert_expr(tree.children[3])
		print(";")


def convert_statements(tree, indent):
	if tree.data == 'statements1':
		if len(tree.children) == 1:
			convert_statement(tree.children[0], indent)
		else:
			convert_statements(tree.children[0], indent)
			convert_statement(tree.children[1], indent)

def convert_procedure(tree):
	convert_type(tree.children[0])

	proc_name = concatenate_leaves(tree.children[1])

	print(" " + proc_name + "(", end="")

	for c in tree.children:
		if type(c) is lark.tree.Tree and c.data[:6] == 'params':
			convert_params(tree.children[3])
			break

	print(") {")

	for c in tree.children:
		if type(c) is lark.tree.Tree and c.data[:4] == 'dcls':
			convert_dcls(c, '\t')
			break

	for c in tree.children:
		if type(c) is lark.tree.Tree and c.data[:9] == 'statement':
			convert_statements(c, '\t')
			break

	print("\treturn ", end="")

	convert_expr(tree.children[-3])

	print(";")

	print("}")

def convert_main(tree):
	p1 = concatenate_leaves(tree.children[4])
	p2 = concatenate_leaves(tree.children[9])

	print("int main(int %s, char** %s) {" % (p1, p2))

	for c in tree.children:
		if type(c) is lark.tree.Tree and c.data[:4] == 'dcls':
			convert_dcls(c, '\t')
			break

	for c in tree.children:
		if type(c) is lark.tree.Tree and c.data[:9] == 'statement':
			convert_statements(c, '\t')
			break

	print("\treturn ", end="")

	convert_expr(tree.children[-3])

	print(";")

	print("}")

def convert_start(tree):
	if tree.data == 'start0':
		convert_procedure(tree.children[0])
		convert_start(tree.children[1])
	elif tree.data == 'start1':
		convert_main(tree.children[0])

def convert(tree):
	print("#include <iostream>")
	print("using namespace std;")

	if tree.data[:5] == 'start':
		convert_start(tree)

