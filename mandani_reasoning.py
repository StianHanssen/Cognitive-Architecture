from math import inf
from collections import Counter

RULES = [(lambda distance, delta: f_and(triangle(distance, 1.5, 4.5),
                                        triangle(delta, 0.5, 3.5)),
         "None"),
         (lambda distance, delta: f_and(triangle(distance, 1.5, 4.5),
                                        triangle(delta, -1.5, 1.5)),
         "SlowDown"),
         (lambda distance, delta: f_and(triangle(distance, 3.5, 6.5),
                                        triangle(delta, 0.5, 3.5)),
         "SpeedUp"),
         (lambda distance, delta: f_and(grade(distance, 7.5, 9),
                                        f_or(f_not(triangle(delta, 0.5, 3.5)),
                                             f_not(grade(delta, 2.5, 4)))),
         "FloorIt"),
         (lambda distance, delta: reverse_grade(distance, 1, 2.5),
         "BrakeHard")]

MEMBERSHIP = [(lambda value: reverse_grade(value, -8, -5), "BrakeHard"),
              (lambda value: triangle(value, -7, -1), "SlowDown"),
              (lambda value: triangle(value, -3, 3), "None"),
              (lambda value: triangle(value, 1, 7), "SpeedUp"),
              (lambda value: grade(value, 5, 8), "FloorIt")]

def f_and(x, y):
    return min(x, y)

def f_or(x, y):
    return max(x, y)

def f_not(x):
    return 1.0 - x

def triangle(position, x0, x2, clip=inf):
    x1 = (x2 + x0) / 2
    value = 0.0
    if position >= x0 and position <= x1:
        value = (position - x0)/(x1 - x0)
    elif position >= x1 and position <= x2:
        value = (x2 - position)/(x1 - x0)
    if value > clip:
        return clip
    return value

def grade(position, x0, x1, clip=inf):
    value = 0.0
    if position >= x1:
        value = 1.0
    elif position <= x0:
        pass
    else:
        value = (position - x0) / (x1 - x0)
    if value > clip:
        return clip
    return value

def reverse_grade(position, x0, x1, clip=inf):
    value = 1.0 - grade(position, x0, x1, clip)
    if value > clip:
        return clip
    return value

def centroid(aggreg_values):
    counted = Counter(aggreg_values).most_common()
    top = 0
    bottom = 0
    for i in range(len(aggreg_values)):
        top += (i - 10) * aggreg_values[i][0]
    for val_pair, instances in counted:
        bottom += val_pair[0] * instances
    if bottom == 0:
        data_sum = 1
    return top / bottom

def get_best_membership(value, aggreg_fuzzy_dict, membership):
    best = (-inf, "undefined")
    for func, action in membership:
        pos = func(value)  # Just used to see if value is in range of action
        val = aggreg_fuzzy_dict[action]
        if pos > 0 and val > best[0]:  # If value is in range of this action and is action is better than any previous choices
            best = (val, action)
    return best

def get_final_action(value, membership):
    best = (-inf, "undefined")
    for func, action in MEMBERSHIP:
        val = func(value)
        if val > best[0]:
            best = (val, action)
    return best[1]

def get_result(distance, delta, rules, membership, samples):
    aggreg_fuzzy_dict = {action: func(distance, delta) for func, action in rules}
    aggreg_values = [get_best_membership(sample, aggreg_fuzzy_dict, membership) for sample in samples]
    centered_value = centroid(aggreg_values)
    return centered_value, get_final_action(centered_value, membership)

print(get_result(3.7, 1.2, RULES, MEMBERSHIP, range(-10, 11)))
