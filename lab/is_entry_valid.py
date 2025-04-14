import re

def is_entry_valid(expr):
    # saco espacios ("_a" lo toma como valido)
    # expr = expr.replace(" ", "")

    # patron para una expresion base: a, b, c, e seguidos opcionalmente de *
    atom = r'(a|b|c|e)\*?'

    # concatenaciones: atom(.atom)*
    concat = fr'{atom}(\.{atom})*'

    # expresiones completas: concat(|concat)*
    full_expr = fr'^{concat}(\|{concat})*$'

    return re.fullmatch(full_expr, expr) is not None