import random
import bisect


class Uniform:
    def __init__(self, min_value, max_value):
        if min_value >= max_value:
            raise Exception("Min value should be less than max value.")
        self.min_value = min_value
        self.max_value = max_value

    def gen(self):
        return self.min_value + int(random.random() * (self.max_value - self.min_value))


class Deterministic:
    def __init__(self, array):
        self.array = array

    def gen(self):
        idx = int(random.random() * len(self.array))
        return self.array[idx]


class Exponential:
    def __init__(self, lamb):
        self.lamb = lamb
        print(f"lamb = {lamb}")

    def gen(self):
        return random.expovariate(self.lamb)


class MonteCarlo:
    def __init__(self, classes_array):
        self.values = [
            (elem['class']['min_value'] + elem['class']['max_value'])/2.0
            for elem in classes_array
        ]
        self.normalize_frequencies(classes_array)
        self.build_accumulated_probs(classes_array)
        # print(f"values: {self.values}")
        # print(f"acc_probs: {self.acc_probs}")

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
