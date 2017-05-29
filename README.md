# Derivative
Парсер выражений. Формула первой производной. 

В файле [parser.py](expression/parser.py) содержится функция `parseExpression(expr)`, которая возвращает объект с методами
* `evaluate(x)` - подсчет значения выражения 
* `derivative()`- получение первой производной 
* Пример использования
```
expr = parseExpression("(x + 2) * cos(x)")
print(expr) # ((x+2.0)*(cos(x)))
print(expr.evaluate(2)) # -1.6645873461885696
print(expr.derivative()) # (((1+0)*(cos(x)))+((x+2.0)*((-((sin(x))))*1)))

