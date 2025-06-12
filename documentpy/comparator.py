import ast

class TypeAnnotationAndDocstringStripper(ast.NodeTransformer):
    """A class that removes type annotations and docstrings from AST nodes."""

    def visit_Module(self, node: ast.Module) -> ast.Module:
        """Visit a module node and strip its docstring."""
        node.body = self.strip_docstring(node.body)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Visit a class definition node and strip its docstring."""
        node.body = self.strip_docstring(node.body)
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Visit a function definition node and strip its docstring."""
        node.returns = None
        self.generic_visit(node)
        node.body = self.strip_docstring(node.body)
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        """Visit an asynchronous function definition node and strip its docstring."""
        node.returns = None
        self.generic_visit(node)
        node.body = self.strip_docstring(node.body)
        return node

    def visit_Lambda(self, node: ast.Lambda) -> ast.Lambda:
        """Visit a lambda node."""
        self.generic_visit(node)
        return node

    def visit_arguments(self, node: ast.arguments) -> ast.arguments:
        """Visit arguments node and strip type annotations."""
        for arg in node.args + node.kwonlyargs:
            arg.annotation = None
        if node.vararg:
            node.vararg.annotation = None
        if node.kwarg:
            node.kwarg.annotation = None
        return node

    def visit_arg(self, node: ast.arg) -> ast.arg:
        """Visit an argument node and strip its type annotation."""
        node.annotation = None
        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.Assign | None:
        """Visit an annotated assignment node and convert it to a regular assignment."""
        if node.value is not None:
            return ast.copy_location(ast.Assign(
                targets=[node.target],
                value=node.value
            ), node)
        return None

    def strip_docstring(self, body: list) -> list:
        """Strip the docstring from the body of a node."""
        if (
            body and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, (ast.Str, ast.Constant))
            and isinstance(getattr(body[0].value, "value", None), str)
        ):
            return body[1:]
        return body

def normalize_ast(code: str) -> ast.AST:
    """Normalize the AST by removing type annotations and docstrings."""
    tree = ast.parse(code)
    tree = TypeAnnotationAndDocstringStripper().visit(tree)
    ast.fix_missing_locations(tree)
    return tree

def is_equivalent(code1: str, code2: str) -> bool:
    """Check if two code snippets are equivalent with the docstrings and type annotations stripped."""
    try:
        tree1 = normalize_ast(code1)
        tree2 = normalize_ast(code2)
        return ast.dump(tree1, annotate_fields=True, include_attributes=False) == \
               ast.dump(tree2, annotate_fields=True, include_attributes=False)
    except SyntaxError:
        return False