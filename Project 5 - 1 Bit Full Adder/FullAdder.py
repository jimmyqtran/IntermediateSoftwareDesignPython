"""
1-bit Full Adder
Jimmy Tran
"""

from abc import ABC, abstractmethod


class CostMixin:
    # Constants
    COST_MULTIPLIER = 10

    def __init__(self, number_of_components):
        self._number_of_components = number_of_components

    @property
    def number_of_components(self):
        return self._number_of_components

    @property
    def cost(self):
        self._cost = self.COST_MULTIPLIER * (self._number_of_components ** 2)
        return self._cost


class NodeMixin:
    def __init__(self):
        self._next = None

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, data):
        if not isinstance(data, NodeMixin):
            raise TypeError("This should be the next NodeMixin, dude")
        self._next = data


class Circuit:
    def __init__(self):
        self._circuit = None
        self._cost = 0

    def add(self, gate):
        if not isinstance(gate, LogicGate):
            raise TypeError("This should be a type of LogicGate, dude")
        if self._circuit is not None:
            gate.next = self._circuit
        self._circuit = gate

    @property
    def cost(self):
        traverse = self._circuit
        while traverse is not None:
            # print(traverse.cost)
            self._cost += traverse.cost
            # print(traverse)
            traverse = traverse.next
            # print(traverse)
        return self._cost


class Input:
    def __init__(self, owner):
        if not isinstance(owner, LogicGate):
            raise TypeError("Own should be a type of LogicGate")
        self._owner = owner

    def __str__(self):
        try:
            return str(self.value)
        except AttributeError:
            # It's possible to not have a value at the beginning
            return "(no value)"

    @property
    def owner(self):
        return self._owner

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # Normalize the value to bool
        self._value = bool(value)
        # Now that the input value has changed, tell to owner logic gate to re-evaluate
        self._owner.evaluate()


class Output:
    def __init__(self):
        self._connections = []

    def __str__(self):
        try:
            return str(self.value)
        except AttributeError:
            # It's possible not to have a value at the beginning
            return "(no value)"

    def connect(self, input):
        if not isinstance(input, Input):
            raise TypeError("Output must be connected to an input")
        # If the input is not already in the list, add it; alternative is to use a set
        if input not in self._connections:
            self._connections.append(input)
        try:
            # Set the input's value to this output's value upon connection
            input.value = self._value
        except AttributeError:
            # If self.value is not there, skip it
            pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # Normalize the value to bool
        self._value = bool(value)
        # After the output value changes, remember to send it to all the connected inputs
        for connection in self._connections:
            connection.value = self.value

    @property
    def connections(self):
        return self._connections


class LogicGate(ABC, NodeMixin):
    def __init__(self, name):
        self._name = name
        NodeMixin.__init__(self)

    @property
    def name(self):
        return self._name

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class UnaryGate(LogicGate, CostMixin):
    def __init__(self, name, number_of_components):
        LogicGate.__init__(self, name)
        CostMixin.__init__(self, number_of_components)
        self._input = Input(self)
        self._output = Output()

    def __str__(self):
        return f"LogicGate {self.name}: input={self.input}, output={self.output}"

    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output


class BinaryGate(LogicGate, CostMixin):
    def __init__(self, name, number_of_components):
        LogicGate.__init__(self, name)
        CostMixin.__init__(self, number_of_components)
        self._input0 = Input(self)
        self._input1 = Input(self)
        self._output = Output()

    def __str__(self):
        return f"LogicGate {self.name}: input0={self.input0}, input1={self.input1}, output={self.output}"

    @property
    def input0(self):
        return self._input0

    @property
    def input1(self):
        return self._input1

    @property
    def output(self):
        return self._output


class NotGate(UnaryGate):
    def __init__(self, name, circuit=None, number_of_components=2):
        UnaryGate.__init__(self, name, circuit)
        CostMixin.__init__(self, number_of_components)
        if circuit is not None:
            if not isinstance(circuit, Circuit):
                raise TypeError("The circuit parameter should be of class Circuit, dude")
            circuit.add(self)

    def evaluate(self):
        self.output.value = not self.input.value


class AndGate(BinaryGate):
    def __init__(self, name, circuit=None, number_of_components=3):
        BinaryGate.__init__(self, name, circuit)
        CostMixin.__init__(self, number_of_components)
        if circuit is not None:
            if not isinstance(circuit, Circuit):
                raise TypeError("The circuit parameter should be of class Circuit, dude")
            circuit.add(self)

    def evaluate(self):
        try:
            # This may throw an exception, if one of the input is not yet set, which is possible
            # in the normal course of evaluation, because setting the first input will kick
            # off the evaluation.  So just don't set the output.
            self.output.value = self.input0.value and self.input1.value
        except AttributeError:
            pass


class OrGate(BinaryGate):
    def __init__(self, name, circuit=None, number_of_components=3):
        BinaryGate.__init__(self, name, circuit)
        CostMixin.__init__(self, number_of_components)
        if circuit is not None:
            if not isinstance(circuit, Circuit):
                raise TypeError("The circuit parameter should be of class Circuit, dude")
            circuit.add(self)

    def evaluate(self):
        try:
            self.output.value = self.input0.value or self.input1.value
        except AttributeError:
            pass


class XorGate(BinaryGate):
    def __init__(self, name, circuit=None, number_of_components=3):
        BinaryGate.__init__(self, name, circuit)
        CostMixin.__init__(self, number_of_components)
        if circuit is not None:
            if not isinstance(circuit, Circuit):
                raise TypeError("The circuit parameter should be of class Circuit, dude")
            circuit.add(self)

    def evaluate(self):
        try:
            # Assume the value is bool, != is same as xor
            self.output.value = (self.input0.value != self.input1.value)
        except AttributeError:
            pass


# This makes sure that the old classes are still functional
def test():
    tests = [test_not, test_and, test_or, test_xor, test_not_not, test_and_not]
    for t in tests:
        print("Running " + t.__name__ + " " + "-" * 20)
        t()


def test_not():
    not_gate = NotGate("not")
    not_gate.input.value = True
    print(not_gate)
    not_gate.input.value = False
    print(not_gate)


def test_and():
    and_gate = AndGate("and")
    print("AND gate initial state:", and_gate)
    and_gate.input0.value = True
    print("AND gate with 1 input set", and_gate)
    and_gate.input1.value = False
    print("AND gate with 2 inputs set:", and_gate)
    and_gate.input1.value = True
    print("AND gate with 2 inputs set:", and_gate)


def test_or():
    or_gate = OrGate("or")
    or_gate.input0.value = False
    or_gate.input1.value = False
    print(or_gate)
    or_gate.input1.value = True
    print(or_gate)


def test_xor():
    # Testing xor
    xor_gate = XorGate("xor")
    xor_gate.input0.value = False
    xor_gate.input1.value = False
    print(xor_gate)
    xor_gate.input1.value = True
    print(xor_gate)


def test_not_not():
    not_gate1 = NotGate("not1")
    not_gate2 = NotGate("not2")
    not_gate1.output.connect(not_gate2.input)
    print(not_gate1)
    print(not_gate2)
    print("Setting not-gate input to False...")
    not_gate1.input.value = False
    print(not_gate1)
    print(not_gate2)


def test_and_not():
    and_gate = AndGate("and")
    not_gate = NotGate("not")
    and_gate.output.connect(not_gate.input)
    and_gate.input0.value = True
    and_gate.input1.value = False
    print(and_gate)
    print(not_gate)
    and_gate.input1.value = True
    print(and_gate)
    print(not_gate)


def abstract_class_test():
    try:
        logic_gate = LogicGate("logic")
        print(logic_gate)
    except TypeError:
        print("Can't instantiate logic gate")
    try:
        unary_gate = UnaryGate("unary")
        print(unary_gate)
    except TypeError:
        print("Can't instantiate unary gate")
    try:
        binary_gate = BinaryGate("binary")
        print(binary_gate)
    except TypeError:
        print("Can't instantiate binary gate")


# Part of the new set of tests for this program
def test2():
    tests2 = [test_not_not_circuit, test_and_not_circuit]
    for s in tests2:
        print("Running " + s.__name__ + " " + "-" * 20)
        s()


def test_not_not_circuit():
    circuit = Circuit()
    not_gate1 = NotGate("not1", circuit)
    not_gate2 = NotGate("not2", circuit)
    not_gate1.output.connect(not_gate2.input)
    print("Cost of NOT-NOT circuit is " + str(circuit.cost))


def test_and_not_circuit():
    circuit2 = Circuit()
    and_gate1 = AndGate("and1", circuit2)
    not_gate3 = NotGate("not3", circuit2)
    and_gate1.output.connect(not_gate3.input)
    print("Cost of AND-NOT circuit is " + str(circuit2.cost))


# 1-bit full adder
def full_adder(a, b, ci):
    # Instantiate the circuit
    circuit_adder = Circuit()

    # sum
    xor_adder_gate1 = XorGate("xor_adder_1", circuit_adder)
    xor_adder_gate1.input0.value = a
    xor_adder_gate1.input1.value = b
    xor_adder_gate2 = XorGate("xor_adder_2", circuit_adder)
    xor_adder_gate1.output.connect(xor_adder_gate2.input0)
    xor_adder_gate2.input1.value = ci
    summation = xor_adder_gate2.output.value

    # co
    and_adder_gate1 = AndGate("and_adder_1", circuit_adder)
    xor_adder_gate1.output.connect(and_adder_gate1.input0)
    and_adder_gate1.input1.value = ci
    and_adder_gate2 = AndGate("and_adder_2", circuit_adder)
    and_adder_gate2.input0.value = a
    and_adder_gate2.input1.value = b
    or_adder_gate1 = OrGate("or_adder_1", circuit_adder)
    and_adder_gate1.output.connect(or_adder_gate1.input0)
    and_adder_gate2.output.connect(or_adder_gate1.input1)
    co = or_adder_gate1.output.value

    # cost
    cost = circuit_adder.cost
    tup = (summation, co, cost)
    return tup


if __name__ == '__main__':
    # Tests from old assignment
    test()
    abstract_class_test()
    try:
        wow = AndGate("try", circuit="potato")
    except TypeError as e:
        print("The TypeError for circuit works: {}".format(e))

    try:
        wow2 = AndGate("try")
        wow2.next = "potato"
    except TypeError as e:
        print("The TypeError for circuit works: {}".format(e))

    try:
        circuit_wow = Circuit()
        circuit_wow.add("potato")
    except TypeError as e:
        print("The TypeError for circuit works: {}".format(e))
    test2()
    print(full_adder(a=True, b=False, ci=True))
