def safe_convert(convert_fn, children, index, name, *args):
	if (index >= len(children)):
		return

	if type(children[index]) is lark.tree.Tree:
		if children[index].data == name:
			convert_fn(children[index], *args)


def concatenate_leaves(tree):
	s = ""

	stack = [tree]
	while len(stack) > 0:
		top = stack.pop()

		if type(top) is lark.lexer.Token:
			s += top.value
		else:
			stack += top.children[::-1]

	return s

def get_type_from_emoji(emoji):
	return "int"

def convert_type(tree):
	type = get_type_from_emoji(concatenate_leaves(tree.children[0]))
	print(type, end="")
	print(concatenate_leaves(tree.children[1]), end="")

def convert_dcl(tree, indent):
	print(indent, end="")
	convert_type(tree.children[0])
	name = concatenate_leaves(tree.children[1])
	print(" " + name, end="")t

def convert_dcls(tree, indent):
	if tree.data == 'decls1':
		convert_dcls(tree.children[0], indent)
		convert_dcl(tree.children[1], indent)
		print(" = %s;" % concatenate_leaves(tree.children[4]))
	elif tree.data == 'decls2':
		convert_dcls(tree.children[0], indent)
		convert_dcl(tree.children[1], indent)
		print(" = NULL;")

def convert_paramlist(tree):
	if tree.data == "paramlist0":
		convert_dcl()

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
		convert_statements(tree.children[5], indent+'\t')
		print(indent + "}")
	elif tree.data == 'statement2':
		print(indent+"while (", end="")
		convert_test(tree.children[1])
		print(") {")
		convert_statements(tree.children[6], indent+'\t')
		print(indent+"}")
	elif tree.data == 'statement3':
		print("cout << ", end="")
		convert_expr(tree.children[2])
		print(";")
	elif tree.data == 'statement4':
		print(indent + "delete[] ", end="")
		convert_expr(tree.children[3])


def convert_statements(tree, indent):
	if tree.data == 'statements1':
		convert_statements(tree.children[0])
		convert_statement(tree.children[1])

def convert_procedure(proc_tree):
	convert_type(proc_tree.children[0])

	proc_name = concatenate_leaves(proc_tree.children[1])

	print(" " + proc_name + "(", end="")

	convert_params(proc_tree.children[3])

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

	convert_expr(proc_tree.children[9])

	print("")

	print("}")

def convert_main(tree):
	p1 = concatenate_leaves(tree.children[4])
	p2 = concatenate_leaves(tree.children[9])

	print("int main(int %s, char** %s) {" % (p1, p2))

	safe_convert(convert_dcls, tree.children, )


def convert(tree):
	print("#include <iostream>")
	print("using namespace std;")

	if tree.data == 'procedures0':
		convert_procedure(tree.children[0])
		convert(tree.children[1])
	elif tree.data == 'procedures1':
		convert_main(tree.children[0])
	elif tree

