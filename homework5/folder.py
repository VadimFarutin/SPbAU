from yat.model import Number, Function, FunctionDefinition,\
                  Conditional, Print, Read, FunctionCall,\
                  Reference, BinaryOperation, UnaryOperation
import yat.printer


class ConstantFolder:
    def visit(self, tree):
        return tree.visit(self)

    def visitNumber(self, number):
        return number

    def visitFunctionDefinition(self, definition):
        visited_expr = []
        if definition.function.body:
            for expr in definition.function.body:
                visited_expr.append(expr.visit(self))
        definition.function.body = visited_expr
        return definition

    def visitConditional(self, conditional):
        conditional.condition = conditional.condition.visit(self)
        visited_expr = []
        if conditional.if_true:
            for expr in conditional.if_true:
                visited_expr.append(expr.visit(self))
        conditional.if_true = visited_expr
        visited_expr = []
        if conditional.if_false:
            for expr in conditional.if_false:
                visited_expr.append(expr.visit(self))
        conditional.if_false = visited_expr
        return conditional

    def visitPrint(self, printer):
        printer.expr = printer.expr.visit(self)
        return printer

    def visitRead(self, reader):
        return reader

    def visitFunctionCall(self, fun_call):
        visited_args = []
        if fun_call.args:
            for arg in fun_call.args:
                visited_args.append(arg.visit(self))
        fun_call.args = visited_args
        return fun_call

    def visitReference(self, reference):
        return reference

    def visitBinaryOperation(self, binary):
        binary.lhs = binary.lhs.visit(self)
        binary.rhs = binary.rhs.visit(self)
        if isinstance(binary.lhs, Number) and isinstance(binary.rhs, Number):
            return Number(binary.operations[binary.op](binary.lhs.value,
                                                       binary.rhs.value))
        if isinstance(binary.rhs, Number) and binary.rhs.value == 0 and\
           isinstance(binary.lhs, Reference) and binary.op is '*':
            return Number(0)
        if isinstance(binary.lhs, Number) and binary.lhs.value == 0 and\
           isinstance(binary.rhs, Reference) and binary.op is '*':
            return Number(0)
        if isinstance(binary.lhs, Reference) and\
           isinstance(binary.rhs, Reference) and\
           binary.op is '-' and binary.lhs.name is binary.rhs.name:
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

    my_printer.visit(conditional_c)
    my_printer.visit(definition_max3_c)
    my_printer.visit(fun_call_c)
    my_printer.visit(definition_log2_c)

if __name__ == '__main__':
    my_tests()
