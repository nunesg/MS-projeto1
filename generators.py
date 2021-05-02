import random


class DummyGenerator:
    def __init__(self, min_time, max_time):
        if min_time >= max_time:
            raise Exception("Min time should be less than max time.")
        self.low = min_time
        self.high = max_time

    def gen(self):
        return self.low + int(random.random() * (self.high - self.low))
