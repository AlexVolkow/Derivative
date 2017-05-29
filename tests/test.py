from math import log, sin, cos, tan, atan, asin, e, pi

ln = lambda x: log(x)
tg = lambda x: tan(x)
ctg = lambda x: 1 / tan(x)
arctg = lambda x: atan(x)
arcsin = lambda x: asin(x)

test_answers = []

absolute_error = 2 ** (-20)
relative_error = 2 ** (-10)


def evaluate_value(function, x):
    return eval(function)


def run_test(solution_answer, jury_answer, test_set, test_info):
    f2 = lambda x: evaluate_value(solution_answer, x)
    f1 = lambda x: evaluate_value(jury_answer, x)
    for x in test_set:
        try:
            y1 = f1(x)
        except:
            continue
        try:
            y2 = f2(x)
        except:
            print("Exception occured. Test input:")
            print(test_info)
            print("Your solution:")
            print(solution_answer)
            print("x = {}, f(x) = {}".format(x, y1))
            exit(0)
        if abs(y1 - y2) > absolute_error and abs(y1 - y2) / max(abs(y1), abs(y2)) > relative_error:
            print("Wrong answer. Test input:")
            print(test_info)
            print("Your solution:")
            print(solution_answer)
            print("x = {}, f(x) = {}, your answer: f(x) = {}".format(x, y1, y2))
            exit(0)


with open('deriv.out', 'r') as file:
    answers = file.readlines()

with open('jury.out', 'r') as file:
    jury_answers = file.readlines()

with open('deriv.in', 'r') as file:
    tests_info = file.readlines()

with open('test_sets', 'r') as file:
    test_sets = [[float(i) for i in line.split()] for line in file.readlines()]

if len(answers) != len(jury_answers):
    print("Wrong number of answers")
    exit(0)

for i in range(len(answers)):
    run_test(answers[i], jury_answers[i], test_sets[i], tests_info[i])
print("Accepted")
