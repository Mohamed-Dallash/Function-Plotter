from PySide2 import QtCore
import pytest
import main
from functionPlotterException import FunctionPlotterException
import time

@pytest.fixture
def app(qtbot):
    app = main.MainWindow()
    qtbot.addWidget(app)
    return app

@pytest.mark.parametrize(
    ("function", "x_min","x_max"),
    (
        ("5*x^3 + 2*x",-10,10),
        ("5*x^3 + 2*x",-100,100),
        ("x^2",-2,5),
        ("2",100,200),
        ("x",-10000,10000)
    )
)
def test_normal_operation(app: main.MainWindow,qtbot,function,x_min,x_max):
    app.expressionTxtBox.setText(function)
    app.xMinTxtBox.setText(str(x_min))
    app.xMaxTxtBox.setText(str(x_max))
    qtbot.mouseClick(app.updatePlotBtn,QtCore.Qt.LeftButton)
    line = app.canvas.axes.lines[0]
    assert line.get_xdata()[0]==x_min
    assert line.get_xdata()[-1]==x_max
    assert len(line.get_xdata()) == 10_000
    assert len(line.get_ydata()) == 10_000

@pytest.mark.parametrize(
    ("x_min","x_max"),
    (
        (1,0),
        (100,-100),
        (10000,0),
        (0,-1)
    )
)
def test_invalid_range(app: main.MainWindow,qtbot,x_min,x_max):
    app.expressionTxtBox.setText("x")
    app.xMinTxtBox.setText(str(x_min))
    app.xMaxTxtBox.setText(str(x_max))
    line = app.canvas.axes.lines[0]
    old_x_data = line.get_xdata()
    old_y_data = line.get_ydata()
    qtbot.mouseClick(app.updatePlotBtn,QtCore.Qt.LeftButton)
    time.sleep(0.5)
    line = app.canvas.axes.lines[0]
    new_x_data = line.get_xdata()
    new_y_data = line.get_ydata()
    #check that nothing was updated in the graph since we have an invalid range
    assert (old_x_data == new_x_data).all()
    assert (old_y_data == new_y_data).all()

@pytest.mark.parametrize(
    ("function"),
    (
        ("/x"),
        (""),
        ("10,0"),
        ("x/")
    )
)
def test_invalid_functions(app: main.MainWindow,qtbot,function):
    app.expressionTxtBox.setText(function)
    line = app.canvas.axes.lines[0]
    old_x_data = line.get_xdata()
    old_y_data = line.get_ydata()
    qtbot.mouseClick(app.updatePlotBtn,QtCore.Qt.LeftButton)
    time.sleep(0.5)
    line = app.canvas.axes.lines[0]
    new_x_data = line.get_xdata()
    new_y_data = line.get_ydata()
    #check that nothing was updated in the graph since we have an invalid function
    assert (old_x_data == new_x_data).all()
    assert (old_y_data == new_y_data).all()
    