import ast
import pprint

tree = ast.parse("x = 4")
pprint.pprint(ast.dump(tree), indent=8)
