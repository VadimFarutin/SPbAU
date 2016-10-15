from yat.model import Number, Function, FunctionDefinition,\
                  Conditional, Print, Read, FunctionCall,\
                  Reference, BinaryOperation, UnaryOperation
import yat.printer
import copy


class ConstantFolder:
    def visit(self, tree):
        return tree.visit(self)

    def visitNumber(self, number):
        return number

    def visitInnerExprs(self, exprs_list):
        visited_exprs = []
        if exprs_list:
            for expr in exprs_list:
                visited_exprs.append(expr.visit(self))
        return visited_exprs

    def visitFunctionDefinition(self, definition):
        new_definition = copy.deepcopy(definition)
        new_definition.function.body = self.visitInnerExprs(definition.function.body)
        return new_definition

    def visitConditional(self, conditional):
        new_conditional = copy.deepcopy(conditional)
        new_conditional.condition = conditional.condition.visit(self)
        new_conditional.if_true = self.visitInnerExprs(conditional.if_true)
        new_conditional.if_false = self.visitInnerExprs(conditional.if_false)
        return new_conditional

    def visitPrint(self, printer):
        new_printer = copy.deepcopy(printer)
        new_printer.expr = printer.expr.visit(self)
        return new_printer

    def visitRead(self, reader):
        return reader

    def visitFunctionCall(self, fun_call):
        new_fun_call = copy.deepcopy(fun_call)
        new_fun_call.args = self.visitInnerExprs(fun_call.args)
        return new_fun_call

    def visitReference(self, reference):
        return reference

    def visitBinaryOperation(self, binary):
        binary.lhs = binary.lhs.visit(self)
        binary.rhs = binary.rhs.visit(self)
        if isinstance(binary.lhs, Number) and isinstance(binary.rhs, Number):
            return Number(binary.operations[binary.op](binary.lhs.value,
                                                       binary.rhs.value))
        if isinstance(binary.rhs, Number) and binary.rhs.value == 0 and\
           isinstance(binary.lhs, Reference) and binary.op == '*':
            return Number(0)
        if isinstance(binary.lhs, Number) and binary.lhs.value == 0 and\
           isinstance(binary.rhs, Reference) and binary.op == '*':
            return Number(0)
        if isinstance(binary.lhs, Reference) and\
           isinstance(binary.rhs, Reference) and\
           binary.op == '-' and binary.lhs.name == binary.rhs.name:
            return Number(0)
        return binary

    def visitUnaryOperation(self, unary):
        unary.expr = unary.expr.visit(self)
        if isinstance(unary.expr, Number):
            return Number(unary.operations[unary.op](unary.expr.value))
        return unary


def my_tests():
    print_binary = Print(
            BinaryOperation(Number(56),
                            '/',
                            UnaryOperation('!',
                                           BinaryOperation(Number(8),
                                                           '%',
                                                           Number(2)))))
    conditional = Conditional(BinaryOperation(BinaryOperation(Number(4),
                                                              '*',
                                                              Number(2)),
                                              '<',
                                              UnaryOperation('-',
                                                             Number(-5))),
                              [print_binary, print_binary],
                              [])
    definition_max3 = FunctionDefinition(
            'max3',
            Function(["a", "b", "c"],
                     [Conditional(
                            BinaryOperation(
                                    Reference("a"),
                                    "-",
                                    Reference("a")),
                            [Conditional(
                                    BinaryOperation(
                                            Reference("a"),
                                            "*",
                                            Number(0)),
                                    [],
                                    [Reference("c")])],
                            [Conditional(
                                    BinaryOperation(
                                            Number(0),
                                            "*",
                                            Reference("c")),
                                    [Reference("c")]
                                    )])
                      ]))
    fun_call = FunctionCall(
            definition_max3,
            [Number(1), BinaryOperation(Number(1), '*', Number(7)), Number(3)])
    definition_log2 = FunctionDefinition(
            "log2",
            Function(["k", "n", "step"],
                     [Conditional(
                              BinaryOperation(
                                      BinaryOperation(
                                              Reference("k"),
                                              "-",
                                              Reference("k")),
                                      "<=",
                                      Reference("n")),
                              [FunctionCall(
                                      Reference("log_2_def"),
                                      [BinaryOperation(
                                                Reference("k"),
                                                "*",
                                                Number(0)),
                                       Reference("n"),
                                       BinaryOperation(
                                                Number(4),
                                                "+",
                                                Number(5))
                                       ])
                               ],
                              [Reference("step")])
                      ]))

    folder = ConstantFolder()
    my_printer = printer.PrettyPrinter()

    conditional_c = folder.visit(conditional)
    definition_max3_c = folder.visit(definition_max3)
    fun_call_c = folder.visit(fun_call)
    definition_log2_c = folder.visit(definition_log2)

    if conditional_c == conditional:
        print('!')
    if definition_max3_c == definition_max3:
        print('!')
    if definition_log2_c == definition_log2:
        print('!')
    if fun_call_c == fun_call:
        print('!')

    my_printer.visit(conditional_c)
    my_printer.visit(conditional)
    my_printer.visit(definition_max3_c)
    my_printer.visit(definition_max3)
    my_printer.visit(fun_call_c)
    my_printer.visit(fun_call)
    my_printer.visit(definition_log2_c)

if __name__ == '__main__':
    my_tests()
