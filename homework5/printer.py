from yat.model import Number, Function, FunctionDefinition,\
                  Conditional, Print, Read, FunctionCall,\
                  Reference, BinaryOperation, UnaryOperation


class PrettyPrinter:
    tab_cnt = 0

    def visit(self, tree):
        tree.visit(self)
        print(';')

    def visitInnerExprs(self, list):
        self.tab_cnt += 1
        if list:
            for expr in list:
                print('\t' * self.tab_cnt, end='')
                expr.visit(self)
                print(';')
        self.tab_cnt -= 1

    def visitNumber(self, number):
        print(str(number.value), end='')

    def visitFunctionDefinition(self, definition):
        print('def ' + definition.name + '(', end='')
        print(', '.join(definition.function.args) + ') {')
        self.visitInnerExprs(definition.function.body)
        print('\t' * self.tab_cnt + '}', end='')

    def visitConditional(self, conditional):
        print('if (', end='')
        conditional.condition.visit(self)
        print(') {')
        self.visitInnerExprs(conditional.if_true)
        print('\t' * self.tab_cnt + '} else {')
        self.visitInnerExprs(conditional.if_false)
        print('\t' * self.tab_cnt + '}', end='')

    def visitPrint(self, printer):
        print('print ', end='')
        printer.expr.visit(self)

    def visitRead(self, reader):
        print('read ' + reader.name, end='')

    def visitFunctionCall(self, fun_call):
        print(fun_call.fun_expr.name + '(', end='')
        if fun_call.args:
            fun_call.args[0].visit(self)
            for arg in fun_call.args[1:]:
                print(', ', end='')
                arg.visit(self)
        print(')', end='')

    def visitReference(self, reference):
        print(reference.name, end='')

    def visitBinaryOperation(self, binary):
        print('(', end='')
        binary.lhs.visit(self)
        print(binary.op, end='')
        binary.rhs.visit(self)
        print(')', end='')

    def visitUnaryOperation(self, unary):
        print('({}'.format(unary.op), end='')
        unary.expr.visit(self)
        print(')', end='')


def my_tests():
    reader = Print(Read('n'))
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
                              [print_binary,
                               UnaryOperation(
                                       '-',
                                       UnaryOperation('!',
                                                      Reference('s')))],
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
    fun_call = Print(FunctionCall(definition_max3, [Number(1), Number(2)]))
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
