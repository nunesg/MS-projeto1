import random
import math
import matplotlib.pyplot as plt


def parse(data):
    data.sort()
    n = len(data)
    min_value, max_value = data[0], data[-1]
    K = round(1 + 3.3*math.log10(n))
    class_len = (max_value - min_value)/K

    # print(f"K: {K}, class_len: {class_len}")
    classes_array = [
        {
            "class": i*class_len + class_len/2.0,
            "frequency": 0
        }
        for i in range(int(max_value/class_len) + 1)
    ]

    idx = 0
    i = 0
    while i < n:
        d2 = 2 * (data[i] - classes_array[idx]["class"])
        # element in class
        if d2 >= -class_len and d2 < class_len:
            classes_array[idx]["frequency"] += 1
            i += 1
        else:
            idx += 1  # change class

    return [elem for elem in classes_array if elem["frequency"] > 0]


def generate_exponential_data(n=10, lamb=0.5):
    return [random.expovariate(lamb) for i in range(n)]
