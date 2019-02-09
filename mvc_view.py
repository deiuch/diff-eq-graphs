import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

from given import x_0_DEFAULT, y_0_DEFAULT, X_DEFAULT, STEP_DEFAULT
from utils import get_color

WINDOW_NAME = 'Numerical method for differential equations solving - graphs'
WINDOW_SIZE = 800, 600
EULER_BTN_TEXT = 'Draw Euler\'s method'
IMPR_EULER_BTN_TEXT = 'Draw Improved Euler\'s method'
RUNGE_KUTTA_BTN_TEXT = 'Draw Runge-Kutta method'
ERROR_BTN_TEXT = 'Change error type'
LBL_x_0_TEXT = 'x_0:'
LBL_y_0_TEXT = 'y_0:'
LBL_X_TEXT = 'X:'
LBL_step_TEXT = 'step:'
EL_NAMES = [
    'plot_left',  # 0
    'plot_right',  # 1
    'x_0_lbl',  # 2
    'y_0_lbl',  # 3
    'X_lbl',  # 4
    'step_lbl',  # 5
    'x_0_inp',  # 6
    'y_0_inp',  # 7
    'X_inp',  # 8
    'step_inp',  # 9
    'euler_btn',  # 10
    'impr_euler_btn',  # 11
    'runge_kutta_btn',  # 12
    'error_btn'  # 13
]


class View(QtGui.QWidget):
    """
    View module of the project for numerical methods of differential equation solving.
    """
    def __init__(self, model, controller):
        """
        :param model: Model module of MVC
        :param controller: Controller module of MVC
        """
        super().__init__(windowTitle=WINDOW_NAME)

        self.model = model
        self.controller = controller
        self.elements = {}
        self._color_iter = get_color()

        # Subscribe on MVC model changes
        model.add_observer(self)

        # Default window properties
        self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        pg.setConfigOptions(antialias=True)

        # Grid elements' initialization
        self.elements[EL_NAMES[0]] = pg.PlotWidget(self, name=EL_NAMES[0])
        self.elements[EL_NAMES[1]] = pg.PlotWidget(self, name=EL_NAMES[1])
        self.elements[EL_NAMES[2]] = QtGui.QLabel(LBL_x_0_TEXT)
        self.elements[EL_NAMES[3]] = QtGui.QLabel(LBL_y_0_TEXT)
        self.elements[EL_NAMES[4]] = QtGui.QLabel(LBL_X_TEXT)
        self.elements[EL_NAMES[5]] = QtGui.QLabel(LBL_step_TEXT)
        self.elements[EL_NAMES[6]] = QtGui.QLineEdit(x_0_DEFAULT)
        self.elements[EL_NAMES[7]] = QtGui.QLineEdit(y_0_DEFAULT)
        self.elements[EL_NAMES[8]] = QtGui.QLineEdit(X_DEFAULT)
        self.elements[EL_NAMES[9]] = QtGui.QLineEdit(STEP_DEFAULT)
        self.elements[EL_NAMES[10]] = QtGui.QPushButton(EULER_BTN_TEXT)
        self.elements[EL_NAMES[11]] = QtGui.QPushButton(IMPR_EULER_BTN_TEXT)
        self.elements[EL_NAMES[12]] = QtGui.QPushButton(RUNGE_KUTTA_BTN_TEXT)
        self.elements[EL_NAMES[13]] = QtGui.QPushButton(ERROR_BTN_TEXT)

        # Adding of elements to the grid
        grid.addWidget(self.elements[EL_NAMES[0]], 0, 0, 1, 4)  # plot_left
        grid.addWidget(self.elements[EL_NAMES[1]], 0, 4, 1, 4)  # plot_right
        grid.addWidget(self.elements[EL_NAMES[2]], 1, 0)  # x_0_lbl
        grid.addWidget(self.elements[EL_NAMES[6]], 1, 1)  # x_0_inp
        grid.addWidget(self.elements[EL_NAMES[3]], 1, 2)  # y_0_lbl
        grid.addWidget(self.elements[EL_NAMES[7]], 1, 3)  # y_0_inp
        grid.addWidget(self.elements[EL_NAMES[4]], 1, 4)  # X_lbl
        grid.addWidget(self.elements[EL_NAMES[8]], 1, 5)  # X_inp
        grid.addWidget(self.elements[EL_NAMES[5]], 1, 6)  # step_lbl
        grid.addWidget(self.elements[EL_NAMES[9]], 1, 7)  # step_inp
        grid.addWidget(self.elements[EL_NAMES[10]], 2, 0, 1, 2)  # euler_btn
        grid.addWidget(self.elements[EL_NAMES[11]], 2, 2, 1, 2)  # impr_euler_btn
        grid.addWidget(self.elements[EL_NAMES[12]], 2, 4, 1, 2)  # runge_kutta_btn
        grid.addWidget(self.elements[EL_NAMES[13]], 2, 6, 1, 2)  # error_btn

        # Subscribe controller to the window elements' actions
        self.elements[EL_NAMES[6]].textChanged.connect(self.controller.x_0_inp_changed)
        self.elements[EL_NAMES[7]].textChanged.connect(self.controller.y_0_inp_changed)
        self.elements[EL_NAMES[8]].textChanged.connect(self.controller.X_inp_changed)
        self.elements[EL_NAMES[9]].textChanged.connect(self.controller.step_inp_changed)
        self.elements[EL_NAMES[10]].clicked.connect(self.controller.euler_btn_pressed)
        self.elements[EL_NAMES[11]].clicked.connect(self.controller.impr_euler_btn_pressed)
        self.elements[EL_NAMES[12]].clicked.connect(self.controller.runge_kutta_btn_pressed)
        self.elements[EL_NAMES[13]].clicked.connect(self.controller.error_btn_pressed)

        self.show()

    def model_has_changed(self):
        """
        Reload graphics according to the new state of the model.
        """
        plots = []
        exact_plot = self.model.exact_plot
        if exact_plot:
            plots.append(exact_plot)
        method_plot = self.model.method_plot
        if method_plot:
            plots.append(method_plot)
        self.update_graph_widget(self.elements[EL_NAMES[0]], plots)

        error_plot = self.model.error_plot
        if error_plot:
            self.update_graph_widget(self.elements[EL_NAMES[1]], [error_plot])
        else:
            self.update_graph_widget(self.elements[EL_NAMES[1]], [])

    def update_graph_widget(self, graph_widget, plots):
        """
        Clear the graph widget and add plots into it.
        :param graph_widget: Widget to clear and update
        :param plots: Iterable containing plots (lists with x's, y's and name)
        """
        graph_widget.getViewBox().removeItem(graph_widget.plotItem.legend)
        graph_widget.clear()
        graph_widget.addLegend()
        for plot_data in plots:
            graph_widget.plot(x=[float(x) for x in plot_data[0]],
                              y=[float(y) for y in plot_data[1]],
                              name=plot_data[2],
                              pen=self._color_iter.__next__())

    def set_inputs_color(self, color_code, *input_field_names):
        """
        Set white color to the pointed fields.
        :param color_code: Color code to set for the fields (for example, 'f6989d')
        :param input_field_names: List of input fields to color white
        """
        for field_name in input_field_names:
            self.elements[field_name].setStyleSheet('QLineEdit {background-color: #%s}' % color_code)
