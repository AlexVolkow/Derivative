from expression.parser import parseExpression

inp = open("deriv.in", "r")
out = open("deriv.out", "w")

for line in inp:
    print(line)
    expr = parseExpression(line.strip())
    out.write(str(expr.derivative()) + "\n")

inp.close()
out.close()
