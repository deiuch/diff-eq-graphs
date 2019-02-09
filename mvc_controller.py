import re

# from fractions import Fraction as Rational
from decimal import Decimal as Rational

from given import get_breakpoints
from mvc_view import View, EL_NAMES
from utils import FLOAT_REGEXP, PlotType, ErrorPlotType

WHITE_CODE = 'ffffff'
SCARLET_CODE = 'f6989d'
BREAKPOINTS = get_breakpoints()


class Controller:
    """
    Controller of user actions of the project for numerical methods of differential equation solving.
    """
    def __init__(self, model):
        """
        :param model: Model module of MVC
        """
        self.model = model
        self.view = None

    def _btn_pressed(self, plot_type, error_type=ErrorPlotType.by_x):
        """
        Check fields and update model fields.
        :param plot_type: Type of plot to draw
        :param error_type: Type of error plot to draw
        """
        inp = []
        for s in EL_NAMES[6:10]:
            inp.append(self.view.elements[s].text())

        # Check inputs for correctness
        if not all(re.match(FLOAT_REGEXP, s) for s in inp) \
                or Rational(inp[0]) in BREAKPOINTS \
                or Rational(inp[2]) in BREAKPOINTS:
            return

        inp = [Rational(x) for x in inp]

        # Check if x_0 is less than X
        if inp[0] >= inp[2]:
            self.view.set_inputs_color(SCARLET_CODE, EL_NAMES[6], EL_NAMES[8])
            return
        self.model.update_inputs(plot_type, error_type, inp[0], inp[1], inp[2], inp[3])

    def euler_btn_pressed(self):
        """
        Action of button 'Draw Euler' pressed.
        """
        self._btn_pressed(PlotType.euler)

    def impr_euler_btn_pressed(self):
        """
        Action of button 'Draw Improved Euler' pressed.
        """
        self._btn_pressed(PlotType.impr_euler)

    def runge_kutta_btn_pressed(self):
        """
        Action of button 'Draw Runge-Kutta' pressed.
        """
        self._btn_pressed(PlotType.runge_kutta)

    def error_btn_pressed(self):
        """
        Action of button 'Change error graph' pressed.
        """
        if self.model.error_type is ErrorPlotType.by_x:
            self._btn_pressed(None, ErrorPlotType.step_dependence)
        else:
            self._btn_pressed(None, ErrorPlotType.by_x)

    def x_0_inp_changed(self):
        """
        Action of text change inside 'x_0' field.
        """
        inp = self.view.elements[EL_NAMES[6]].text()
        if re.match(FLOAT_REGEXP, inp) and Rational(inp) not in BREAKPOINTS:
            self.view.set_inputs_color(WHITE_CODE, EL_NAMES[6], EL_NAMES[8])
        else:
            self.view.set_inputs_color(SCARLET_CODE, EL_NAMES[6])

    def y_0_inp_changed(self):
        """
        Action of text change inside 'y_0' field.
        """
        inp = self.view.elements[EL_NAMES[7]].text()
        self.view.set_inputs_color(
            WHITE_CODE if re.match(FLOAT_REGEXP, inp) else SCARLET_CODE,
            EL_NAMES[7]
        )

    def X_inp_changed(self):
        """
        Action of text change inside 'X' field.
        """
        inp = self.view.elements[EL_NAMES[8]].text()
        if re.match(FLOAT_REGEXP, inp) and Rational(inp) not in BREAKPOINTS:
            self.view.set_inputs_color(WHITE_CODE, EL_NAMES[6], EL_NAMES[8])
        else:
            self.view.set_inputs_color(SCARLET_CODE, EL_NAMES[8])

    def step_inp_changed(self):
        """
        Action of text change inside 'step' field.
        """
        inp = self.view.elements[EL_NAMES[9]].text()
        self.view.set_inputs_color(
            WHITE_CODE if re.match(FLOAT_REGEXP, inp) else SCARLET_CODE,
            EL_NAMES[9]
        )
