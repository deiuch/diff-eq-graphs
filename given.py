# y' = f(x, y)
# y(x_0) = y_0
# x in [x_0; X]

# All the calculations should be done using this type
# from fractions import Fraction as Rational
from decimal import Decimal as Rational

e = Rational('2.7182818284590452353602874713')  # 28 first digits after point (Wikipedia)

# IVP constants - Variant 4
# ATTENTION! If changing x_0 or y_0 => change y_ivp function!
x_0_DEFAULT = '1.0'
y_0_DEFAULT = '1.0'
X_DEFAULT = '10.0'
STEP_DEFAULT = '0.01'
_BREAKPOINTS = ['0.0']


def get_breakpoints():
    """
    Breakpoints of a given function from the Variant 4.
    :return: Breakpoint Rational x value
    """
    return [Rational(x) for x in _BREAKPOINTS]


def f(x, y):
    """
    Given function f(x, y) for Variant 4.
    :param x: x value
    :param y: y value
    :return: f(x, y) value with given x and y
    """
    return 1 + y * (2 * x - 1) / x ** 2


def y(x, c):
    """
    Original function y(x) of differential equation from the Variant 4.
    :param x: x value
    :param c: initial coefficient
    :return: y(x, c) value with given x value and c coefficient
    """
    return (x ** 2) * (1 + c * (e ** (1 / x)))


def c(x, y):
    """
    Calculating of IVP coefficient for function y(x, c) from the Variant 4.
    :param x: x_0 value
    :param y: y_0 value
    :return: coefficient value c for y(x, c)
    """
    return (y - x ** 2) / ((x ** 2) * e ** (1 / x))


def y_ivp(x):
    """
    Function y(x) of differential equation from Variant 4 with solved IVP for y(1) = 1.
    Note: same as call y(x, c) with c = 0
    :param x: x value
    :return: y(x) value with given x value
    """
    return x ** 2
