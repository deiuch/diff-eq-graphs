# Variant 4
# y' = f(x, y)
# y(x_0) = y_0
# x in [x_0; X]

# from fractions import Fraction as Rational
from decimal import Decimal as Rational
from enum import Enum

from given import f, y, c, y_ivp, x_0_DEFAULT, y_0_DEFAULT

COLORS = [
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (0, 0, 255),
    (127, 127, 127),
    (255, 255, 255)
]
FLOAT_REGEXP = r'^(-?)(0|([1-9][0-9]*))(\.[0-9]+)?$'
MAX_STEPS_NUMBER = 100


class PlotType(Enum):
    exact = 0
    euler = 1
    impr_euler = 2
    runge_kutta = 3


class ErrorPlotType(Enum):
    by_x = 0
    step_dependence = 1


def rational_range(start, stop=None, step=Rational(1)):
    """
    Rational version of range().
    Return an object that produces a sequence of Rational objects from start (inclusive)
    to stop (exclusive) by step. frange(i, j, k) produces i, i+k, i+2*k, ...
    start defaults to 0.0, and stop is omitted! range(3.9) produces 0.0, 1.0, 2.0, 3.0.
    When step is given, it specifies the increment (or decrement).
    :param start: Initial value (included)
    :param stop: Final value (excluded)
    :param step: Step of a sequence
    :return: Rational number - next element of the sequence
    """
    if stop is None:
        stop = start
        start = Rational(0)
    while start < stop if step > 0 else start > stop:
        yield start
        start += step


def exact(x_0, y_0, start, end, step):
    """
    Exact solution of the equation y' = f(x, y)
    with IVP for given y(x_0) = y_0 for x in [x_0, X].
    :param x_0: x value if IVP
    :param y_0: y value for the corresponding x_0 value
    :param start: Start x value
    :param end: Last x value
    :param step: Frequency step (dx) - how often x is counted
    :return: Tuple: x values, y values
    """
    xs = []
    ys = []
    if x_0 == x_0_DEFAULT and y_0 == y_0_DEFAULT:
        for x in rational_range(start, end + step, step):
            xs.append(x)
            ys.append(y_ivp(x))
    else:
        cur_c = c(x_0, y_0)
        for x in rational_range(start, end + step, step):
            xs.append(x)
            ys.append(y(x, cur_c))
    return xs, ys


def euler(x_0, y_0, start, end, step):
    """
    Solution of the equation y' = f(x, y) using Euler's method
    with IVP for given y(x_0) = y_0 for x in [x_0, X].
    :param x_0: x value if IVP
    :param y_0: y value for the corresponding x_0 value
    :param start: Start x value
    :param end: Last x value
    :param step: Frequency step (dx) - how often x is counted
    :return: Tuple: x values, y values
    """
    xs = [x_0]
    ys = [y_0]
    if start != x_0:
        xs = [start]
        ys = [y(start, c(x_0, y_0))]
    for i, x in enumerate(rational_range(start + step, end + step, step)):
        xs.append(x)
        ys.append(ys[i] + (x - xs[i]) * f(xs[i], ys[i]))
    return xs, ys


def euler_improved(x_0, y_0, start, end, step):
    """
    Solution of the equation y' = f(x, y) using Improved Euler's method
    with IVP for given y(x_0) = y_0 for x in [x_0, X].
    :param x_0: x value if IVP
    :param y_0: y value for the corresponding x_0 value
    :param start: Start x value
    :param end: Last x value
    :param step: Frequency step (dx) - how often x is counted
    :return: Tuple: x values, y values
    """
    xs = [x_0]
    ys = [y_0]
    if start != x_0:
        xs = [start]
        ys = [y(start, c(x_0, y_0))]
    for i, x in enumerate(rational_range(start + step, end + step, step)):
        xs.append(x)
        y_pred = ys[i] + (x - xs[i]) * f(xs[i], ys[i])
        ys.append(ys[i] + (x - xs[i]) * (f(xs[i], ys[i]) + f(x, y_pred)) / 2)
    return xs, ys


def runge_kutta(x_0, y_0, start, end, step):
    """
    Solution of the equation y' = f(x, y) using Runge-Kutta method (RK4, fourth-order)
    with IVP for given y(x_0) = y_0 for x in [x_0, X].
    :param x_0: x value if IVP
    :param y_0: y value for the corresponding x_0 value
    :param start: Start x value
    :param end: Last x value
    :param step: Frequency step (dx) - how often x is counted
    :return: Tuple: x values, y values
    """
    xs = [x_0]
    ys = [y_0]
    if start != x_0:
        xs = [start]
        ys = [y(start, c(x_0, y_0))]
    for i, x in enumerate(rational_range(start + step, end + step, step)):
        xs.append(x)
        k1 = f(xs[i], ys[i])
        k2 = f(xs[i] + step / 2, ys[i] + step * k1 / 2)
        k3 = f(xs[i] + step / 2, ys[i] + step * k2 / 2)
        k4 = f(xs[i] + step, ys[i] + step * k3)
        ys.append(ys[i] + step * (k1 + 2 * k2 + 2 * k3 + k4) / 6)
    return xs, ys


def error_between(ys1, ys2):
    """
    Calculate error of one function's results in compare to other's.
    :param ys1: y values of the 1st function
    :param ys2: y values of the 2nd function
    :return: differences between the corresponding y values of functions
    """
    return [abs(y1 - y2) for y1, y2 in zip(ys1, ys2)]


def max_errors(func1, func2, breakpoints, x_0, y_0, X, max_steps_number=MAX_STEPS_NUMBER):
    """
    Calculate max error values of two functions for different step sizes.
    :param func1: Original function
    :param func2: Function with some error comparing to the original one
    :param breakpoints: Set of breakpoints of functions on the x axis
    :param x_0: x value of IVP
    :param y_0: y value for the corresponding x_0 value
    :param X: Last x value of calculating range of functions
    :param max_steps_number: Number of steps for the very last calculation
    :return: Tuple: n values (number of steps), y values (max error for n)
    """
    ns = []
    max_err_values = []
    for n in range(1, int(max_steps_number) + 1):
        ns.append(n)
        cur_step = Rational(str((X - x_0) / n))
        errors = []
        last_break = x_0

        # Find errors between breakpoints
        for bkpt in breakpoints:
            errors += error_between(
                func1(x_0, y_0, last_break, bkpt - cur_step, cur_step)[1],
                func2(x_0, y_0, last_break, bkpt - cur_step, cur_step)[1]
            )
            last_break = bkpt + cur_step

        # Find errors after the last breakpoint
        errors += error_between(
            func1(x_0, y_0, last_break, X, cur_step)[1],
            func2(x_0, y_0, last_break, X, cur_step)[1]
        )

        max_err_values.append(max(errors))

    return ns, max_err_values


def get_color():
    """
    Get next color from cyclic list of colors.
    :return: Next color tuple in RGB format
    """
    i = 0
    while True:
        yield COLORS[i]
        i += 1
        if i == len(COLORS):
            i = 0
