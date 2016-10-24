from random import randint
from pprint import PrettyPrinter
import itertools

def gen_inputs(function, num_inputs):
    final_input = []
    x_inputs = [list(map(int, seq)) for seq in itertools.product("01", repeat=num_inputs)]
    for x in x_inputs:
        x.append(function(x))
        final_input.append(tuple(x))
    return final_input

class nerve_network:
    def __init__(inputs, init_thresh):
        self.thresh = init_thresh
        self.inputs = inputs
        self.weights = [randint(-5, 5)/10 for _ in range(len(inputs))]

    def Y(self, p):
        exp = self.inputs[p][:-1]
        return sum([exp[i] * self.weights[i] - self.thresh for i in range(len(exp))])

pp = PrettyPrinter()
pprint(gen_inputs(lambda x: x[0] & x[1], 2))
