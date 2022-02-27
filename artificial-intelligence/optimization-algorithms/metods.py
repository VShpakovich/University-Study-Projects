# Steepest gradient descent, gradient descent and Newton metods implementation
# Author: Valeryia Shpakovich


import numpy as np
import math
import random


# Rosenbrock function
def function(x, y):
    return(1-x)**2 + 100*(y-x*x)**2


def gradient(x, y):
    derivative_x = -400*x*(-x**2 + y) + 2*x-2
    derivative_y = -200*x**2 + 200*y
    return(np.array([derivative_x, derivative_y]))


def hessian(x, y):
    derivative_x_x = 1200*x**2-400*y + 2
    derivative_y_x = -400*x
    hess = [[derivative_x_x, -400],
            [derivative_y_x, 200]]
    return (np.array(hess))


# finding the step size for which
# the value of Rosenbrock function f(x - step*d) will be minimal
phi = (1.0 + math.sqrt(5.0))/2.0


def golden_section(x, d, a, b, epsilon=1e-12):
    x1 = b - (b-a)/phi
    x2 = a + (b-a)/phi
    while((b-a)/2 > epsilon):
        if function((x-x1*d)[0], (x-x1*d)[1]) > function((x-x2*d)[0], (x-x2*d)[1]):
            a = x1
            x1 = x2
            x2 = b - (x1 - a)
        else:
            b = x2
            x2 = x1
            x1 = a + (b - x2)
    return (a+b)/2


# For tests methods return final point and number of iterations
def steepest_gradient_descent(x0, max_number_of_iterations=10000, epsilon=1e-12, step=1):
    x = x0
    i = 0
    d = gradient(x[0], x[1])
    while i < max_number_of_iterations and np.linalg.norm(d) > epsilon:
        d = gradient(x[0], x[1])
        step = golden_section(x, d, 0, 1)
        x = x - step*d
        i += 1
        # print("iteration ", i, " point ", x)
    point = np.array([round(x[0], 2), round(x[1], 2)])
    return point, i


def newton_method(x0, max_number_of_iterations=10000, epsilon=1e-12, step=1):
    x = x0
    i = 0
    d = gradient(x[0], x[1])
    while i < max_number_of_iterations and np.linalg.norm(d) > epsilon:
        d = gradient(x[0], x[1])
        h = hessian(x[0], x[1])
        h_inv = np.linalg.inv(h)
        x = x - h_inv.dot(d) * step
        i += 1
        # print("iteration ", i, " point ", x)
    point = np.array([round(x[0], 2), round(x[1], 2)])
    return point, i


def gradient_descent(x0, max_number_of_iterations=10000, epsilon=1e-12, step=0.0001):
    x = x0
    i = 0
    d = gradient(x[0], x[1])
    while i < max_number_of_iterations and np.linalg.norm(d) > epsilon:
        d = gradient(x[0], x[1])
        x = x - step*d
        i += 1
        print("iteration ", i, " point ", x)
    point = np.array([round(x[0], 2), round(x[1], 2)])
    return point, i

##################


# Test methods
def generate_points(n):
    points = []
    for i in range(n):
        x = random.randint(-5, 5)
        y = random.randint(-5, 5)
        point = np.array([x, y])
        points.append(point)
    return points


def result_for_each_point(points, method, number_of_iterations=10000, epsilon=1e-12,step=1):
    iterations = []
    results = []
    for point in points:
        results.append(method(point, number_of_iterations, epsilon, step)[0])
        iterations.append(method(point, number_of_iterations, epsilon, step)[1])
    return results, iterations
