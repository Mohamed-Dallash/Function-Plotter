from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,QLineEdit,QMessageBox,QLabel,QPushButton
from PySide2.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from functionPlotterException import FunctionPlotterException
from expressionGenerator import ExpressionGenerator
import numpy as np

expressionGenerator = ExpressionGenerator()

def getDataPoints(function,x_min,x_max):
    x_data = []
    y_data = []
    for x in np.linspace(x_min,x_max,10_000).tolist():
        x_data.append(x)
        try:
            val = eval(function)
        except ZeroDivisionError:
            # raise FunctionPlotterException(type="Math Error",message="One or more of the evaluations of the function has a division by zero")
            val = np.nan
        if isinstance(val,complex):
            raise FunctionPlotterException(type="Math Error",message="One or more of the evaluations of the function yields an imaginary number\nTry eliminating fractional powers or limit the range to use only positive numbers")
        y_data.append(val)
    return x_data,y_data

class MatplotlibCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.supxlabel('x')
        fig.supylabel('F(x)')
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("f(x)")
        super(MatplotlibCanvas, self).__init__(fig)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.mainWidget = QWidget()
        self.layout = QVBoxLayout()
        self.canvas = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        self.expressionBox = QHBoxLayout()
        self.expressionLbl = QLabel("F(x)=")
        self.expressionTxtBox = QLineEdit()
        self.expressionTxtBox.setText("5*x^3 + 2*x")
        self.expressionBox.addWidget(self.expressionLbl)
        self.expressionBox.addWidget(self.expressionTxtBox)

        self.rangeControlBox = QHBoxLayout()
        self.xMinLbl = QLabel("x Min:")
        self.xMaxLbl = QLabel("x Max:")
        self.xMinTxtBox = QLineEdit()
        self.xMaxTxtBox = QLineEdit()
        self.xMinTxtBox.setText("-100")
        self.xMaxTxtBox.setText("100")
        self.xMinTxtBox.setValidator(QDoubleValidator())
        self.xMaxTxtBox.setValidator(QDoubleValidator())
        self.rangeControlBox.addWidget(self.xMinLbl)
        self.rangeControlBox.addWidget(self.xMinTxtBox)
        self.rangeControlBox.addWidget(self.xMaxLbl)
        self.rangeControlBox.addWidget(self.xMaxTxtBox)

        self.updatePlotBtn = QPushButton("Update Plot")
        self.updatePlotBtn.clicked.connect(self.updatePlot)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)

        self.layout.addWidget(self.canvas)
        self.layout.addLayout(self.expressionBox)
        self.layout.addLayout(self.rangeControlBox)
        self.layout.addWidget(self.updatePlotBtn)
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle("Function Plotter")
        self.updatePlot()
        self.show()
    
    def getExpression(self):
        expression = expressionGenerator.generateExpression(function=self.expressionTxtBox.text())
        return expression

    def getRange(self):
        if not len(self.xMinTxtBox.text()):
            raise FunctionPlotterException(type="Range Error",message="The value for for \"x Min\" cannot be blank")
        if not len(self.xMaxTxtBox.text()):
            raise FunctionPlotterException(type="Range Error",message="The value for for \"x Max\" cannot be blank")
        x_min = float(self.xMinTxtBox.text())
        x_max = float(self.xMaxTxtBox.text())
        if x_min>=x_max:
            raise FunctionPlotterException(type="Range Error",message="The value for for \"x Max\" should be greater than the value of \"x Min\"")
        return x_min, x_max#, step
    
    def updatePlot(self):
        try:
            function = self.getExpression()
            x_min, x_max = self.getRange()
            x,y=getDataPoints(function=function,x_min=x_min,x_max=x_max)
            self.canvas.axes.cla()  # Clear the canvas
            self.canvas.axes.plot(x,y)
            self.canvas.draw()
        except FunctionPlotterException as e:
            self.showError(type=e.type,message=e.message)
        except Exception as e:
            self.showError(type=str(e.__class__.__name__),message=str(e))

    def showError(self, type, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText(type)
        msg.setInformativeText(message)
        msg.setWindowTitle(type)
        msg.exec_()

if __name__ == "__main__":
        app = QApplication([])
        win = MainWindow()
        win.show()
        app.exec_()
