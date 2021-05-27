import ast
s = "{'1': '2'}"

print(s)
print(str(s))
print(type(s))
print(type(ast.literal_eval(s)))