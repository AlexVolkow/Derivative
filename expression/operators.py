from enum import Enum
import math


class Const:
    def __init__(self, val):
        self.val = val

    def evaluate(self, x):
        return self.val

    def __str__(self):
        return str(self.val)

    def derivative(self):
        return Const(0)


class Variable:
    def __init__(self, name):
        self.name = name

    def evaluate(self, x):
        return x

    def __str__(self):
        return self.name

    def derivative(self):
        return Const(1)


class BinaryOperator:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, x):
        return self.calc(self.left.evaluate(x), self.right.evaluate(x))

    def __str__(self):
        return '(' + str(self.left) + self.op() + str(self.right) + ')'


class UnaryOperator:
    def __init__(self, arg):
        self.arg = arg

    def evaluate(self, x):
        return self.calc(self.arg.evaluate(x))

    def __str__(self):
        return '(' + self.op() + '(' + str(self.arg) + '))'

    def derivative_impl(self):
        raise NotImplementedError("'You must override the method \'derivImpl\'")

    def derivative(self):
        return Multiply(self.derivative_impl(), self.arg.derivative())


class Negate(UnaryOperator):
    def op(self):
        return '-'

    def calc(self, v):
        return -v

    def derivative_impl(self):
        return Negate(self.arg.derivative())


class Add(BinaryOperator):
    def op(self):
        return '+'

    def calc(self, x, y):
        return x + y

    def derivative(self):
        return Add(self.left.derivative(), self.right.derivative())


class Substract(BinaryOperator):
    def op(self):
        return '-'

    def calc(self, x, y):
        return x - y

    def derivative(self):
        return Substract(self.left.derivative(), self.right.derivative())


class Multiply(BinaryOperator):
    def op(self):
        return '*'

    def calc(self, x, y):
        return x * y

    def derivative(self):
        return Add(Multiply(self.left.derivative(), self.right), Multiply(self.left, self.right.derivative()))


class Divide(BinaryOperator):
    def op(self):
        return '/'

    def calc(self, x, y):
        return x / y

    def derivative(self):
        return Divide(
            Substract(Multiply(self.left.derivative(), self.right), Multiply(self.left, self.right.derivative())),
            Pow(self.right, 2))


class Sin(UnaryOperator):
    def op(self):
        return 'sin'

    def calc(self, v):
        return math.sin(v)

    def derivative_impl(self):
        return Cos(self.arg)


class Cos(UnaryOperator):
    def op(self):
        return 'cos'

    def calc(self, v):
        return math.cos(v)

    def derivative_impl(self):
        return Negate(Sin(self.arg))


class Pow(BinaryOperator):
    def op(self):
        return '**'

    def calc(self, x, y):
        return x ** y

    def derivative(self):
        if not (isinstance(self.left, Const)) and isinstance(self.right, Const):
            return Multiply(Multiply(Pow(self.left, Const(self.right.val - 1)), self.right),self.left.derivative())
        if isinstance(self.left, Const) and not (isinstance(self.right, Const)):
            return Multiply(Multiply(self, Ln(self.left)),self.right.derivative())
        if isinstance(self.left, Const) and isinstance(self.right, Const):
            return Const(0)
        if not (isinstance(self.left, Const)) and not (isinstance(self.right, Const)):
            return Exp(Multiply(Ln(self.left), self.right)).derivative()


class Tg(UnaryOperator):
    def op(self):
        return 'tg'

    def calc(self, v):
        return math.tg(v)

    def derivative_impl(self):
        return Divide(Const(1), Pow(Cos(self.arg), 2))


class Ctg(UnaryOperator):
    def op(self):
        return 'ctg'

    def calc(self, v):
        return math.ctg(v)

    def derivative_impl(self):
        return Divide(Negate(Const(1)), Pow(Sin(self.arg), 2))


class Arcsin(UnaryOperator):
    def op(self):
        return 'arcsin'

    def calc(self, v):
        return math.arcsin(v)

    def derivative_impl(self):
        return Divide(Const(1), Pow(Substract(Const(1), Pow(self.arg, 2)), 0.5))


class Arctg(UnaryOperator):
    def op(self):
        return 'arctg'

    def calc(self, v):
        return math.arctg(v)

    def derivative_impl(self):
        return Divide(Const(1), Add(Const(1), Pow(self.arg, 2)))


class Ln(UnaryOperator):
    def op(self):
        return 'ln'

    def calc(self, v):
        return math.ln(v)

    def derivative_impl(self):
        return Divide(Const(1), self.arg)


class Exp(UnaryOperator):
    def op(self):
        return 'e**'

    def calc(self, v):
        return math.e ** v

    def derivative_impl(self):
        return Exp(self.arg)


class Operator(Enum):
    variable = 1
    const = 2
    add = 3
    substract = 4
    multiply = 5
    divide = 6
    sin = 7
    cos = 8
    power = 9
    tg = 10
    ctg = 11
    arcsin = 12
    arctg = 13
    ln = 14
    exp = 15
    left_br = 16
    right_br = 17
