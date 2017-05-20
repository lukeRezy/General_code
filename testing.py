import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random

def plot_data():

    data = [[1,2,3,4], [4,3,2,1]]

    class Window(QDialog):
        def __init__(self, parent=None):
            super(Window, self).__init__(parent)

            for i in range(len(data)):
                # a figure instance to plot on
                self.figure = plt.figure()

                # this is the Canvas Widget that displays the `figure`
                # it takes the `figure` instance as a parameter to __init__
                self.canvas = FigureCanvas(self.figure)

                # this is the Navigation widget
                # it takes the Canvas widget and a parent
                self.toolbar = NavigationToolbar(self.canvas, self)

                self.plot(i)

                # set the layout
                layout = QVBoxLayout()
                layout.addWidget(self.toolbar)
                layout.addWidget(self.canvas)
            self.setLayout(layout)

        def plot(self, i):
            ''' plot some random stuff '''
            # random data

            # create an axis
            ax1 = self.figure.add_subplot(111)
            ax2 = ax1.twinx()

            # discards the old graph
            # ax.hold(False) # deprecated, see above

            # plot data
            ax1.plot(data[i], '*-')

            # refresh canvas
            self.canvas.draw()





    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    plot_data()