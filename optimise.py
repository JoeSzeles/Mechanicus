
from math import sqrt
from datetime import datetime as dt
from utils import *


def get_distance(a, b, sq=False):
    x1, y1 = a[0], a[1]
    x2, y2 = b[0], b[1]

    x = x2 - x1
    y = y2 - y1

    if sq:
        return sqrt(x * x + y * y)
    else:
        return x * x + y * y


def get_total_distance(shapes):
    
    total_distance = 0
    last = list(shapes).pop(0)[-1]

    for i in shapes:
        total_distance += get_distance(i[0], last, sq=True)

    return total_distance


def optimise_path(shapes, sq=False):

    t1 = dt.now()
    new_order = []
    new_order.append(shapes.pop(0))
    l = len(shapes)
    while len(new_order) <= l:

        shortest = float("Inf")
        last = new_order[-1][-1]

        for shape in shapes:

            d = get_distance(last, shape[0], sq)
            d2 = get_distance(last, shape[-1], sq)

            if d < shortest:
                shortest = d
                selection = shape
                reverse = False

            if d2 < shortest:
                shortest = d2
                reverse = True
                selection = shape

        if reverse:
            new_order.append([x for x in reversed(selection)])
        else:
            new_order.append(selection)
        shapes.remove(selection)

    timer(t1, "optimizing       ")
    return new_order

