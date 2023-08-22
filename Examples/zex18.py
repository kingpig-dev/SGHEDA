import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow
import numpy as np

# Create some sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create the application and main window
app = QApplication([])
window = QMainWindow()

# Create a plot widget
plot_widget = pg.PlotWidget()

# Add the plot widget to the main window
window.setCentralWidget(plot_widget)

# Create a plot item
plot_item = plot_widget.getPlotItem()

# Create plot curves for each series and add them to the plot item
curve1 = plot_item.plot(x, y1, pen='r', name='Series 1')
curve2 = plot_item.plot(x, y2, pen='g', name='Series 2')

# Set plot labels
plot_item.setLabel('left', 'Y')
plot_item.setLabel('bottom', 'X')

# Create a legend item
legend = pg.LegendItem()
legend.setParentItem(plot_item)

# Add the curves and their names to the legend
legend.addItem(curve1, 'Series 1')
legend.addItem(curve2, 'Series 2')

legend.anchor((0,0), (0.1,0.8))

# Show the main window
window.show()

# Start the application event loop
app.exec_()