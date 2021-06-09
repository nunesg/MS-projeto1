import random
import bisect
import montecarlo
from math import pi, log, sqrt, cos, sin


class Uniform:
    def __init__(self, min_value, max_value):
        if min_value >= max_value:
            raise Exception(
                "Min value should be less or equal than max value.")
        self.min_value = min_value
        self.max_value = max_value
        self.uniform_inverse = lambda r, a, b: a + r*(b-a)

    def gen(self):
        return self.uniform_inverse(random.random(), self.min_value, self.max_value)


class UniformInt(Uniform):
    def __init__(self, min_value, max_value):
        super().__init__(int(min_value), int(max_value))

    def gen(self):
        return int(self.gen(random.random(), self.min_value, self.max_value+1))


class Deterministic:
    def __init__(self, value):
        self.value = value

    def gen(self):
        return self.value


class Normal:
    def __init__(self, mean, std_deviation):
        self.mean = mean
        self.std_deviation = std_deviation
        self.idx = 2
        self.values = [0, 0]
        self.zcos = lambda r1, r2: cos(2 * pi * r2)*sqrt(-2 * log(r1))
        self.zsin = lambda r1, r2: sin(2 * pi * r2)*sqrt(-2 * log(r1))

    def reset_values(self):
        self.idx = self.idx % 2
        if self.idx != 0:
            return
        r1 = random.random()
        r2 = random.random()
        self.values = [self.zcos(r1, r2), self.zsin(r1, r2)]

    def z(self):
        self.reset_values()
        val = self.values[self.idx]
        self.idx += 1
        return val

    def gen(self):
        return abs(self.std_deviation * self.z() + self.mean)


class Exponential:
    def __init__(self, lamb):
        self.lamb = lamb
        self.inverse_exponential = lambda r: -(log(1 - r)/self.lamb)

    def gen(self):
        return self.inverse_exponential(random.random())


class MonteCarlo:
    def __init__(self, values):
        classes_array = montecarlo.parse(values)
        # print(classes_array)
        self.values = [elem['class'] for elem in classes_array]
        self.normalize_frequencies(classes_array)
        self.build_accumulated_probs(classes_array)

    def gen(self):
        idx = bisect.bisect_left(self.acc_probs, random.random())
        return self.values[idx]

    def normalize_frequencies(self, classes_array):
        total_sum = 0
        for elem in classes_array:
            total_sum += elem['frequency']

        for elem in classes_array:
            elem['frequency'] /= total_sum

    def build_accumulated_probs(self, classes_array):
        self.acc_probs = []
        acc = 0.0
        for elem in classes_array:
            acc += elem['frequency']
            self.acc_probs.append(acc)
