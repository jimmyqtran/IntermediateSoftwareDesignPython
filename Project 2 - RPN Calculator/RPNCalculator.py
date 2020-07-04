"""
RPN Calculator
Jimmy Tran
"""
import numpy as np


class MyStack:
    # Constants
    MAX_CAPACITY = 100000
    DEFAULT_CAPACITY = 10

    # Initializer method
    def __init__(self, default_item, capacity=DEFAULT_CAPACITY):
        # If the capacity is bad, fail right away
        if not self.validate_capacity(capacity):
            raise ValueError("Capacity " + str(capacity) + " is invalid")
        self.capacity = capacity
        self.default_item = default_item

        # Make room in the stack and make sure it's empty to begin with
        self.clear()

    def clear(self):
        # Allocate storage the storage and initialize top of stack
        self.stack = np.array([self.default_item for _ in range(self.capacity)])
        self.top_of_stack = 0

    @classmethod
    def validate_capacity(cls, capacity):
        return 0 <= capacity <= cls.MAX_CAPACITY

    def push(self, item_to_push):
        if self.is_full():
            raise IndexError("Push failed - capacity reached")
        self.stack[self.top_of_stack] = item_to_push
        self.top_of_stack += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop failed - stack is empty")

        self.top_of_stack -= 1
        return self.stack[self.top_of_stack]

    def is_empty(self):
        return self.top_of_stack == 0

    def is_full(self):
        return self.top_of_stack == self.capacity

    def get_capacity(self):
        return self.capacity

    # Suggested by the professor to aid in debugging process
    def __str__(self):
        return "Stack: {}\nTop of Stack: {}" \
            .format(self.stack, self.top_of_stack)


class RpnCalculator:
    # Constants
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    FLOOR_DIVISION = "//"

    # # Initializer method
    # def __init__(self, rpn_expression):
    #     self.rpn_expression = rpn_expression

    @staticmethod
    def multiply(a, b):
        if b == 0:
            return 0
        elif b > 0:
            return a + RpnCalculator.multiply(a, b - 1)
        elif b < 0:
            return -RpnCalculator.multiply(a, -b)

    @staticmethod
    def parse(rpn_expression):
        li = list(rpn_expression.split(" "))
        return li

    @staticmethod
    def eval_tokens(tokens):
        pancake = MyStack(-1)
        operand = 0
        operator = 0
        for i in tokens:
            try:
                i = int(i)
                operand += 1
                pancake.push(i)
            except ValueError:
                if not i:
                    raise ValueError("Empty string")
                if i not in [RpnCalculator.ADDITION, RpnCalculator.SUBTRACTION,
                             RpnCalculator.MULTIPLICATION, RpnCalculator.FLOOR_DIVISION]:
                    raise ValueError("Unknown operator {}".format(i))
                else:
                    operator += 1
                    b = pancake.pop()
                    a = pancake.pop()
                    if i == RpnCalculator.ADDITION:
                        c = int(a + b)
                        pancake.push(c)
                    elif i == RpnCalculator.SUBTRACTION:
                        c = int(a - b)
                        pancake.push(c)
                    elif i == RpnCalculator.FLOOR_DIVISION:
                        c = int(a // b)
                        pancake.push(c)
                    elif i == RpnCalculator.MULTIPLICATION:
                        c = int(RpnCalculator.multiply(a, b))
                        pancake.push(c)
        if operand == operator + 1:
            result = pancake.pop()
            return result
        elif operand > operator + 1:
            raise ValueError("Not enough operators")
        elif operand <= operator:
            raise ValueError("Not enough operands")

    @staticmethod
    def eval(rpn_expression):
        parsed = RpnCalculator.parse(rpn_expression)
        result = RpnCalculator.eval_tokens(parsed)
        return result


def test_rpn():
    test_list = [
        # Single number
        "3",
        # multiply() check (zeros, double zeros, negatives, double negatives)
        "0 0 *", "0 4 *", "0 -3 *", "4 0 *", "-3 0 *",
        "-5 2 *", "5 -2 *", "-5 -2 *",
        # An expression for each of the 4 supported operations
        "3 6 +", "3 6 -", "3 6 *", "3 6 //",
        # 3 or more increasingly complex expressions that consist of multiple operations(e.g. "2 3 4 + *")
        "1 1 1 + -",
        "22 3 2 * // 4 7 9 * * *",
        "15 7 1 1 + - // 3 * 2 1 1 + + -",
        "1 8 1 5 * - - 3 + 2 1 1 // - + 5 * 4 5 + *",
        # Expression with invalid operator
        "1 1 fly", "random junk",
        # Empty string
        "",
        # Expression with insufficient operator (two integers followed by no operator, e.g."1 1")
        "1 1",
        # Expression with insufficient operands (zero or one integer followed by an operator, e.g."1 +")
        "4 +", "4 + +",
    ]

    for test in test_list:
        try:
            result = RpnCalculator.eval(test)
            print("({}) = {}" .format(test, result))
        except Exception as e:
            print("\"" + test + "\" failed to be evaluated: {}".format(e))


if __name__ == "__main__":
    test_rpn()
