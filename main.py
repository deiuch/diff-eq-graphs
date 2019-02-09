from pyqtgraph.Qt import QtGui, QtCore

import mvc_controller
import mvc_model
import mvc_view


def main():
    app = QtGui.QApplication([])
    model = mvc_model.Model()
    controller = mvc_controller.Controller(model)
    view = mvc_view.View(model, controller)

    controller.view = view
    view.show()
    app.exec()


if __name__ == '__main__':
    main()
