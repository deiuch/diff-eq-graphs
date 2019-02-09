from given import get_breakpoints
from utils import exact, euler, euler_improved, runge_kutta, error_between, max_errors, ErrorPlotType, PlotType

METHODS = {
    PlotType.exact: exact,
    PlotType.euler: euler,
    PlotType.impr_euler: euler_improved,
    PlotType.runge_kutta: runge_kutta
}
GRAPH_NAMES = {
    PlotType.exact: 'Exact solution',
    PlotType.euler: 'Euler\'s method',
    PlotType.impr_euler: 'Improved Euler\'s method',
    PlotType.runge_kutta: 'Runge-Kutta method',
    ErrorPlotType.by_x: 'Difference with the exact solution',
    ErrorPlotType.step_dependence: 'Maximum error for different step sizes'
}


class Model:
    """
    Logical model of the project for numerical methods of differential equation solving.
    """
    def __init__(self):
        self._x_0 = None
        self._y_0 = None
        self._X = None
        self._step = None
        self._exact_plot = None
        self._method_plot = None
        self._method_type = PlotType.euler
        self._error_plot = None
        self.error_type = ErrorPlotType.by_x
        self._observers = []

    @property
    def exact_plot(self):
        if not self._exact_plot:
            return None
        return self._exact_plot

    @property
    def method_plot(self):
        return self._method_plot

    @property
    def error_plot(self):
        return self._error_plot

    def update_inputs(self, method_type, error_type, x_0, y_0, X, step):
        """
        Change the state of the model by changing all the parameters of it.
        :param method_type: Enumerable of graph type to be shown; if None - previous to be used
        :param error_type: Enumerable of error graph type to be shown; if None - previous to be used
        :param x_0: x_0 parameter
        :param y_0: y_0 parameter
        :param X: X parameter
        :param step: step parameter
        """
        changed = self._x_0 != x_0
        self._x_0 = x_0
        changed |= self._y_0 != y_0
        self._y_0 = y_0
        changed |= self._X != X
        self._X = X
        changed |= self._step != step
        self._step = step
        if method_type:
            changed |= self._method_type != method_type
            self._method_type = method_type
        if error_type:
            changed |= self.error_type != error_type
            self.error_type = error_type
        if changed:
            self._calculate_functions()
            self._notify_observers()

    def _clear_data(self):
        """
        Make empty all plot data.
        """
        self._exact_plot = [[], [], '']
        self._method_plot = [[], [], '']
        self._error_plot = [[], [], '']

    def add_observer(self, observer):
        """
        Add new observer of changes in model to the notify list.
        WARNING: It should have an attribute 'model_has_changed()'.
        :param observer: New observer to be added
        """
        assert hasattr(observer, 'model_has_changed')
        self._observers.append(observer)

    def remove_observer(self, observer):
        """
        Remove an observer from the notify list.
        :param observer: Observer to be removed
        """
        self._observers.remove(observer)

    def _notify_observers(self):
        """
        Send notification to all the subscribers that the model has changed.
        """
        for o in self._observers:
            o.model_has_changed()

    def _calculate_functions(self):
        """
        Refresh functions dictionary according to the values x_0, y_0, X and step.
        """
        breakpoints = get_breakpoints()
        i = 0
        while i < len(breakpoints):
            if not self._x_0 < breakpoints[i] < self._X:
                breakpoints = breakpoints[:i] + breakpoints[i + 1:]
            else:
                i += 1

        x_0 = self._x_0
        y_0 = self._y_0
        X = self._X
        step = self._step
        last_break = x_0

        self._clear_data()

        # Calculating parts of the function between the breakpoints
        for bkpt in breakpoints:
            exact_sol = METHODS[PlotType.exact](x_0, y_0, last_break, bkpt - step, step)
            self._exact_plot[0] += exact_sol[0]
            self._exact_plot[1] += exact_sol[1]

            method_sol = METHODS[self._method_type](x_0, y_0, last_break, bkpt - step, step)
            self._method_plot[0] += method_sol[0]
            self._method_plot[1] += method_sol[1]

            last_break = bkpt + step

        # Calculation of part after the last breakpoint
        exact_sol = METHODS[PlotType.exact](x_0, y_0, last_break, X, step)
        self._exact_plot[0] += exact_sol[0]
        self._exact_plot[1] += exact_sol[1]

        method_sol = METHODS[self._method_type](x_0, y_0, last_break, X, step)
        self._method_plot[0] += method_sol[0]
        self._method_plot[1] += method_sol[1]

        # Calculating error of method's solution comparably to the exact solution
        if self.error_type is ErrorPlotType.by_x:
            self._error_plot[0] = self._exact_plot[0].copy()
            self._error_plot[1] = error_between(self._exact_plot[1], self._method_plot[1])
        elif self.error_type is ErrorPlotType.step_dependence:
            max_errors_plot = max_errors(
                METHODS[PlotType.exact],
                METHODS[self._method_type],
                breakpoints,
                x_0, y_0, X,  # TODO change max_steps_number
            )
            self._error_plot[0] = max_errors_plot[0]
            self._error_plot[1] = max_errors_plot[1]

        self._exact_plot[2] = GRAPH_NAMES[PlotType.exact]
        self._method_plot[2] = GRAPH_NAMES[self._method_type]
        self._error_plot[2] = GRAPH_NAMES[self.error_type]
