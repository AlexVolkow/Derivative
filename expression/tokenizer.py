from expression.operators import Operator


def tokenize(expr):
    def nextWord(i, f):
        start = i
        while i < len(expr) and f(expr[i]):
            i += 1
        return expr[start:i]

    def nextToken(i):
        return nextWord(i, lambda c: not (c.isspace()) and c != '(' and c != ')' and not (c.isdigit()))

    def nextNumber(i):
        return nextWord(i, lambda c: c.isdigit() or c == 'e' or c == '.')

    def makeToken(typeToken, val):
        return {'type': typeToken, 'value': val}

    tokens = []
    i = 0
    while i < len(expr):
        while i < len(expr) and expr[i].isspace():
            i += 1
        if i == len(expr):
            break
        if expr[i] == '(':
            tokens.append(makeToken(Operator.left_br, expr[i]))
            i += 1
            continue
        if expr[i] == ')':
            tokens.append(makeToken(Operator.right_br, expr[i]))
            i += 1
            continue
        if not (expr[i].isdigit()) and expr[i] != 'e':
            token = nextToken(i)
            typeToken = {
                '+': Operator.add,
                '-': Operator.substract,
                '*': Operator.multiply,
                '/': Operator.divide,
                'sin': Operator.sin,
                'cos': Operator.cos,
                'ln': Operator.ln,
                '**': Operator.power,
                'tg': Operator.tg,
                'ctg': Operator.ctg,
                'arcsin': Operator.arcsin,
                'arctg': Operator.arctg,
                'x': Operator.variable,
                'e': Operator.const,
            }[token]
        else:
            token = nextNumber(i)
            typeToken = Operator.const
        tokens.append(makeToken(typeToken, token))
        i += len(token)
    return tokens
