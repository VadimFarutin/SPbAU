class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.dict = {}

    def __setitem__(self, name, value):
        self.dict[name] = value

    def __getitem__(self, name):
        if self.dict.get(name, None) is None and self.parent is not None:
            return self.parent[name]
        return self.dict.get(name, None)


class Number:
    def __init__(self, value):
        self.value = int(float(value))

    def evaluate(self, scope):
        return self


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        result = None
        for expression in self.body:
            result = expression.evaluate(scope)
        return result


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        function = self.function
        if isinstance(self.function, Reference):
            function = self.function.evaluate(scope)
        scope[self.name] = function
        return function


class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if self.condition.evaluate(scope).value == 0:
            branch = self.if_false
        else:
            branch = self.if_true
        result = None
        if branch is not None:
            for expression in branch:
                result = expression.evaluate(scope)
        return result


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        value = self.expr.evaluate(scope).value
        print(value)
        return Number(value)


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        number = Number(input())
        scope[self.name] = number
        return number


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for name, value in zip(function.args, self.args):
            call_scope[name] = value.evaluate(scope)
        return function.evaluate(call_scope)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        left_value = self.lhs.evaluate(scope).value
        right_value = self.rhs.evaluate(scope).value
        if self.op == "+":
            value = left_value + right_value
        elif self.op == "-":
            value = left_value - right_value
        elif self.op == "*":
            value = left_value * right_value
        elif self.op == "/":
            value = left_value // right_value
        elif self.op == "%":
            value = left_value % right_value
        elif self.op == "==":
            value = left_value == right_value
        elif self.op == "!=":
            value = left_value != right_value
        elif self.op == "<":
            value = left_value < right_value
        elif self.op == ">":
            value = left_value > right_value
        elif self.op == "<=":
            value = left_value <= right_value
        elif self.op == ">=":
            value = left_value >= right_value
        elif self.op == "&&":
            value = left_value and right_value
        else:
            value = left_value or right_value
        return Number(value)


class UnaryOperation:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        value = self.expr.evaluate(scope).value
        if self.op == "-":
            return Number(-value)
        return Number(value == 0)


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def my_tests():
    main = Scope()
    main["div"] = UnaryOperation("-", BinaryOperation(Number(10), "/", Number(20))).evaluate(main)
    print("-(10/20) =", main["div"].value)
    main["div"] = BinaryOperation(UnaryOperation("-", Number(10)), "/", Number(20)).evaluate(main)
    print("(-10)/20 =", main["div"].value)
    main["div"] = BinaryOperation(Number(10), "/", Number(20)).evaluate(main)
    print("10/20 =", main["div"].value)

    '''LOG_2'''
    main["abs"] = Function(["value"],
                           [Conditional(
                                  BinaryOperation(
                                          Reference("value"),
                                          "<",
                                          Number(0)),
                                  [UnaryOperation(
                                          "-",
                                          Reference("value"))],
                                  [Reference("value")])])
    main["log_2_func"] = Function(["k", "n", "step"],
                                  [Conditional(
                                          BinaryOperation(
                                                  BinaryOperation(
                                                          Reference("k"),
                                                          "*",
                                                          Number(2)),
                                                  "<=",
                                                  Reference("n")),
                                          [FunctionCall(
                                                  FunctionDefinition(
                                                          "log_2_func",
                                                          Reference("log_2_func")),
                                                  [BinaryOperation(
                                                            Reference("k"),
                                                            "*",
                                                            Number(2)),
                                                   Reference("n"),
                                                   BinaryOperation(
                                                            Reference("step"),
                                                            "+",
                                                            Number(1))
                                                   ])
                                           ],
                                          [Reference("step")])
                                   ])
    main["print"] = Function(["value"], [Print(Reference("value"))])
    print('LOG_2')
    print(' Print n: ', end=' ')
    Read("n").evaluate(main)
    main["abs_n"] = FunctionCall(
            FunctionDefinition("abs", main["abs"]),
            [main["n"]]).evaluate(main)
    main["log_2"] = FunctionCall(
            FunctionDefinition("log_2_func", main["log_2_func"]),
            [Number(1), main["abs_n"], Number(0)]).evaluate(main)
    print(' log_2(|'+str(main["n"].evaluate(main).value)+'|): ', end=' ')
    FunctionCall(
            FunctionDefinition("print", main["print"]),
            [main["log_2"]]).evaluate(main)

    '''MAX3'''
    main["max3"] = Function(["a", "b", "c"],
                            [Conditional(
                                    BinaryOperation(
                                            Reference("a"),
                                            ">",
                                            Reference("b")),
                                    [Conditional(
                                            BinaryOperation(
                                                    Reference("a"),
                                                    ">=",
                                                    Reference("c")),
                                            [Reference("a")],
                                            [Reference("c")])],
                                    [Conditional(
                                            BinaryOperation(
                                                    Reference("b"),
                                                    "<",
                                                    Reference("c")),
                                            [Reference("c")],
                                            [Reference("b")])])
                             ])
    print('MAX3')
    print(' Print first: ', end=' ')
    Read("first").evaluate(main)
    print(' Print second: ', end=' ')
    Read("second").evaluate(main)
    print(' Print third: ', end=' ')
    Read("third").evaluate(main)
    main["max"] = FunctionCall(
            FunctionDefinition("max3", main["max3"]),
            [main["first"], main["second"], main["third"]]).evaluate(main)
    print(' max: ', end=' ')
    FunctionCall(
            FunctionDefinition("print", main["print"]),
            [main["max"]]).evaluate(main)

    '''EVEN AND POSITIVE'''
    main["is_even_pos"] = Function(["n"],
                                   [Conditional(
                                        BinaryOperation(
                                                UnaryOperation(
                                                        "!",
                                                        BinaryOperation(
                                                                Reference("n"),
                                                                "%",
                                                                Number(2))),
                                                "&&",
                                                BinaryOperation(
                                                        Reference("n"),
                                                        ">",
                                                        Number(0))),
                                        [Number(1)],
                                        [Number(0)])
                                    ])
    print('EVEN AND POSITIVE')
    print(' Print n: ', end=' ')
    Read("n").evaluate(main)
    main["res"] = FunctionCall(
            FunctionDefinition("is_even_pos", main["is_even_pos"]),
            [main["n"]]).evaluate(main)
    print(' Is '+str(main["n"].evaluate(main).value)+' even and positive? : ',
          end=' ')
    FunctionCall(
            FunctionDefinition("print", main["print"]),
            [main["res"]]).evaluate(main)

if __name__ == '__main__':
    example()
    my_tests()
