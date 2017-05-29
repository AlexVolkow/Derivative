from expression.operators import *
from expression.tokenizer import tokenize


def parseExpression(expr):
    tokens = tokenize(expr)
    operator = {'+': {'op': Add, 'priority': 1}, '-': {'op': Substract, 'priority': 1},
                '*': {'op': Multiply, 'priority': 2}, '/': {'op': Divide, 'priority': 2},
                '**': {'op': Pow, 'priority': 2}}
    index = -1

    def primary():
        nonlocal index
        index += 1
        tokenType = tokens[index]['type']

        if tokenType == Operator.variable:
            return Variable('x')
        if tokenType == Operator.const:
            return Const(float(tokens[index]['value']))

        if tokenType == Operator.left_br:
            pr = expression()
            index += 1
            return pr

        if tokenType == Operator.substract:
            if index < len(tokens) - 1 and tokens[index + 1]['type'] == Const:
                index += 1
                return Const(float('-' + tokens[index]['value']))
            else:
                index -= 1
                return Multiply(Const(-1), primary())

        acc = {
            Operator.sin: Sin,
            Operator.cos: Cos,
            Operator.ln: Ln,
            Operator.tg: Tg,
            Operator.ctg: Ctg,
            Operator.arcsin: Arcsin,
            Operator.arctg: Arctg
        }[tokenType]
        index += 1
        expr = acc(expression())
        index += 1
        return expr

    def make_stage(priority, nextStage):
        def temp():
            nonlocal index
            acc = nextStage()
            while index < len(tokens) - 1:
                index += 1
                if not (tokens[index]['value'] in operator):
                    index -= 1
                    return acc

                token = operator[tokens[index]['value']]
                oper = token['op']
                if token['priority'] == priority:
                    acc = oper(acc, nextStage())
                else:
                    index -= 1
                    return acc
            return acc
        return temp

    term = make_stage(2, primary)
    expression = make_stage(1, term)
    return expression()
