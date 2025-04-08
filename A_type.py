# Define the classes for the AST
class Expr:
    pass

class Var(Expr):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Lambda(Expr):
    def __init__(self, var, body):
        self.var = var    # parameter (a Var)
        self.body = body  # body (an Expr)

    def __repr__(self):
        return f"(λ{self.var}.{self.body})"

class App(Expr):
    def __init__(self, func, arg):
        self.func = func  # function (an Expr)
        self.arg = arg    # argument (an Expr)

    def __repr__(self):
        return f"({self.func} {self.arg})"


# A simple recursive-descent parser.
# It expects a string like "λx.x", or "((λx.x) y)".
# Note: This parser assumes single-letter variable names and no spaces.
def parse(expr_str):
    expr_str = expr_str.replace(" ", "")  # remove spaces
    pos = 0

    def parse_expr():
        nonlocal pos
        # An expression could be a lambda abstraction or an application chain.
        if pos < len(expr_str) and expr_str[pos] in ("λ", "\\"):
            return parse_lambda()
        else:
            return parse_app()

    def parse_lambda():
        nonlocal pos
        # Consume the lambda symbol
        if expr_str[pos] not in ("λ", "\\"):
            raise SyntaxError("Expected lambda")
        pos += 1  # skip λ
        # Get the variable (assume single letter)
        if pos >= len(expr_str) or not expr_str[pos].isalpha():
            raise SyntaxError("Expected a variable after lambda")
        var = Var(expr_str[pos])
        pos += 1
        # Expect a dot
        if pos >= len(expr_str) or expr_str[pos] != ".":
            raise SyntaxError("Expected dot after lambda variable")
        pos += 1
        body = parse_expr()
        return Lambda(var, body)

    def parse_app():
        nonlocal pos
        # Parse a sequence of factors (variables, parenthesized expressions, or lambdas) that associate to the left.
        left = parse_factor()
        while pos < len(expr_str) and expr_str[pos] not in (")", "."):
            right = parse_factor()
            left = App(left, right)
        return left

    def parse_factor():
        nonlocal pos
        if pos >= len(expr_str):
            raise SyntaxError("Unexpected end of input")
        if expr_str[pos] == "(":
            pos += 1  # skip '('
            exp = parse_expr()
            if pos >= len(expr_str) or expr_str[pos] != ")":
                raise SyntaxError("Expected ')'")
            pos += 1  # skip ')'
            return exp
        elif expr_str[pos] in ("λ", "\\"):
            return parse_lambda()
        elif expr_str[pos].isalpha():
            var = Var(expr_str[pos])
            pos += 1
            return var
        else:
            raise SyntaxError(f"Unexpected character: {expr_str[pos]}")

    parsed = parse_expr()
    if pos != len(expr_str):
        raise SyntaxError("Extra characters after valid expression")
    return parsed


# Substitution function: substitute var 'v' with expression 'sub' in expression 'expr'.
def substitute(expr, v, sub):
    if isinstance(expr, Var):
        # If it's the variable v, substitute; otherwise, leave it.
        return sub if expr.name == v.name else expr
    elif isinstance(expr, Lambda):
        # If the lambda's variable is the same as v, do not substitute in the body.
        if expr.var.name == v.name:
            return expr
        else:
            return Lambda(expr.var, substitute(expr.body, v, sub))
    elif isinstance(expr, App):
        return App(substitute(expr.func, v, sub), substitute(expr.arg, v, sub))
    else:
        raise TypeError("Unexpected expression type.")


# Perform one beta reduction step.
def beta_reduce(expr):
    # If the expression is an application and its function is a lambda abstraction, reduce it.
    if isinstance(expr, App) and isinstance(expr.func, Lambda):
        # (λv.body) arg  ==> body[v := arg]
        return substitute(expr.func.body, expr.func.var, expr.arg), True

    # Otherwise, try to reduce inside the expression recursively.
    if isinstance(expr, App):
        new_func, reduced = beta_reduce(expr.func)
        if reduced:
            return App(new_func, expr.arg), True
        new_arg, reduced = beta_reduce(expr.arg)
        if reduced:
            return App(expr.func, new_arg), True
    elif isinstance(expr, Lambda):
        new_body, reduced = beta_reduce(expr.body)
        if reduced:
            return Lambda(expr.var, new_body), True

    return expr, False


# Repeatedly reduce until no beta reductions can be applied.
def full_beta_reduce(expr):
    current = expr
    changed = True
    while changed:
        current, changed = beta_reduce(current)
    return current


# A new version of LambdaBetaReduce that uses the parser and reduction:
def LambdaBetaReduce(string_lambda):
    try:
        parsed = parse(string_lambda)
    except SyntaxError as e:
        print("Syntax error:", e)
        return None
    print("Parsed expression:", parsed)
    reduced = full_beta_reduce(parsed)
    print("Reduced expression:", reduced)
    return reduced


# Example usage:
# For instance, the beta reduction of "((λx.x) y)" should yield "y".
if __name__ == '__main__':
    # Some sample expressions. For example:
    # Identity: λx.x
    # Application: ((λx.x) y) should reduce to y.
    # You might adjust your syntax—here we expect something like:
    expr_input = "((λx.x)y)"
    result = LambdaBetaReduce(expr_input)
    input("Press Enter to exit...")
