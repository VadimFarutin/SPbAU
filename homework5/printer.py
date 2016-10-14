from yat.model import Number, Function, FunctionDefinition,\
                  Conditional, Print, Read, FunctionCall,\
                  Reference, BinaryOperation, UnaryOperation


class PrettyPrinter:
    tab_cnt = 0

    def visit(self, tree):
        tree.visit(self)
        print(';')

    def visitNumber(self, number):
        print('\t' * self.tab_cnt + str(number.value), end='')

    def visitFunctionDefinition(self, definition):
        print('\t' * self.tab_cnt + 'def ' + definition.name + '(', end='')
        print(', '.join(definition.function.args) + ') {')
        self.tab_cnt += 1
        for expr in definition.function.body:
            expr.visit(self)
            print(';')
        self.tab_cnt -= 1
        print('\t' * self.tab_cnt + '}', end='')

    def visitConditional(self, conditional):
        print('\t' * self.tab_cnt + 'if (', end='')
        tabs = self.tab_cnt
        self.tab_cnt = 0
        conditional.condition.visit(self)
        self.tab_cnt = tabs
        print(') {')
        self.tab_cnt += 1
        for expr in conditional.if_true:
            expr.visit(self)
            print(';')
        self.tab_cnt -= 1
        print('\t' * self.tab_cnt + '} else {')
        self.tab_cnt += 1
        for expr in conditional.if_false:
            expr.visit(self)
            print(';')
        self.tab_cnt -= 1
        print('\t' * self.tab_cnt + '}', end='')

    def visitPrint(self, printer):
        print('\t' * self.tab_cnt + 'print ', end='')
        tabs = self.tab_cnt
        self.tab_cnt = 0
        printer.expr.visit(self)
        self.tab_cnt = tabs

    def visitRead(self, reader):
        print('\t' * self.tab_cnt + 'read ' + reader.name, end='')

    def visitFunctionCall(self, fun_call):
        print('\t' * self.tab_cnt + fun_call.fun_expr.name + '(', end='')
        tabs = self.tab_cnt
        self.tab_cnt = 0
        if fun_call.args:
            fun_call.args[0].visit(self)
            for arg in fun_call.args[1:]:
                print(', ', end='')
                arg.visit(self)
        self.tab_cnt = tabs
        print(')', end='')

    def visitReference(self, reference):
        print('\t' * self.tab_cnt + reference.name, end='')

    def visitBinaryOperation(self, binary):
        print('\t' * self.tab_cnt + '(', end='')
        binary.lhs.visit(self)
        print(binary.op, end='')
        binary.rhs.visit(self)
        print(')', end='')

    def visitUnaryOperation(self, unary):
        print('\t' * self.tab_cnt + '({}'.format(unary.op), end='')
        unary.expr.visit(self)
        print(')', end='')


def my_tests():
    reader = Read('n')
    print_binary = Print(
            BinaryOperation(Reference('x'),
                            '/',
                            UnaryOperation('!',
                                           BinaryOperation(Reference('y'),
                                                           '%',
                                                           Number(2)))))
    conditional = Conditional(BinaryOperation(BinaryOperation(Reference('x'),
                                                              '*',
                                                              Number(2)),
                                              '<',
                                              UnaryOperation('-',
                                                             Reference('y'))),
                              [print_binary, print_binary],
                              [])
    definition_max3 = FunctionDefinition(
            'max3',
            Function(["a", "b", "c"],
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
                      ]))
    fun_call = FunctionCall(definition_max3, [Number(1)])
    definition_log2 = FunctionDefinition(
            "log2",
            Function(["k", "n", "step"],
                     [Conditional(
                              BinaryOperation(
                                      BinaryOperation(
                                              Reference("k"),
                                              "*",
                                              Number(2)),
                                      "<=",
                                      Reference("n")),
                              [FunctionCall(
                                      Reference("log_2_def"),
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
                      ]))
    empty_func = FunctionDefinition("emptyFunc", Function([], []))
    printer = PrettyPrinter()
    printer.visit(reader)
    printer.visit(conditional)
    printer.visit(print_binary)
    printer.visit(definition_max3)
    printer.visit(fun_call)
    printer.visit(definition_log2)
    printer.visit(empty_func)

if __name__ == '__main__':
    my_tests()
