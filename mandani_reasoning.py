from math import inf
from collections import Counter


__author__ = "Stian R. Hanssen"

#Dynamic rule set and membership functions
#----------------------------------------#
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

ACTION_FUNCS = [(lambda value, clip=inf: reverse_grade(value, -8, -5, clip), "BrakeHard"),
                (lambda value, clip=inf: triangle(value, -7, -1, clip), "SlowDown"),
                (lambda value, clip=inf: triangle(value, -3, 3, clip), "None"),
                (lambda value, clip=inf: triangle(value, 1, 7, clip), "SpeedUp"),
                (lambda value, clip=inf: grade(value, 5, 8, clip), "FloorIt")]

#Fuzzy logical operators
#----------------------#
def f_and(x, y):
    return min(x, y)

def f_or(x, y):
    return max(x, y)

def f_not(x):
    return 1.0 - x

#Mathematical functions for shapes on a graph
#-------------------------------------------#
def triangle(x_value, x_start, x_end, clip=inf):
    x_mid = (x_end + x_start) / 2
    y_value = 0.0
    if x_value >= x_start and x_value <= x_mid:
        y_value = (x_value - x_start)/(x_mid - x_start)
    elif x_value >= x_mid and x_value <= x_end:
        y_value = (x_end - x_value)/(x_mid - x_start)
    if y_value > clip:
        return clip
    return y_value

def grade(x_value, x_start, x_end, clip=inf):
    y_value = 0.0
    if x_value >= x_end:
        y_value = 1.0
    elif x_value <= x_start:
        pass
    else:
        y_value = (x_value - x_start) / (x_end - x_start)
    if y_value > clip:
        return clip
    return y_value

def reverse_grade(x_value, x_start, x_end, clip=inf):
    y_value = 1.0 - grade(x_value, x_start, x_end, clip)
    if y_value > clip:
        return clip
    return y_value

#Functions for calculating the fuzzy logic it self
#------------------------------------------------#
def centroid(aggregated_values, first_sample_value):
    counted = Counter(aggregated_values).most_common()
    top = 0
    bottom = 0
    for i in range(len(aggregated_values)):
        top += (i + first_sample_value) * aggregated_values[i]  # 'sample x value' * 'y_value in action for samnple x value'
    for value, instances in counted:
        bottom += value * instances  # 'y value' * 'number of instances of this value'
    if bottom == 0:  # Avoid dividing by zero, will result in a less accurate answer
        bottom = 1
    return top / bottom

#Finds y value in the aggregated fuzzy set for x position value
def get_aggregated_value(value, clip_values, action_funcs):
    best = -inf
    for func, action in action_funcs:  # Finds highest y value if actons overlap at x position value
        clip = clip_values[action]
        val = func(value, clip)
        if val > best:
            best = val
    return best

#Finds action with the highest y value for given x position value
def get_action(value, action_funcs):
    best = (-inf, "undefined")
    for func, action in action_funcs:
        val = func(value)
        if val > best[0]:
            best = (val, action)
    return best[1]

#Executes the mandani reasoning based on the given values, set of rules, membership functions and sampling of the aggregated fuzzy set
def get_result(distance, delta, rules, action_funcs, samples):
    clip_values = {action: func(distance, delta) for func, action in rules}
    aggregated_values = [get_aggregated_value(sample, clip_values, action_funcs) for sample in samples]
    centered_value = centroid(aggregated_values, samples[0])
    return centered_value, get_action(centered_value, action_funcs)

print(get_result(3.7, 1.2, RULES, ACTION_FUNCS, range(-10, 11)))
#Output:
#(-0.3529411764705879, 'None')
