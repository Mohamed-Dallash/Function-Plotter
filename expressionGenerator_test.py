import pytest
from expressionGenerator import ExpressionGenerator
from functionPlotterException import FunctionPlotterException

expressionGenerator = ExpressionGenerator()

@pytest.mark.parametrize(
    ("input", "expected"),
    (
        ("x^2","x**2"),
        ("x + 2    ","x+2"),
        ("1. ","1."),
        (" x/2 *x","x/2*x"),
        ("x^2^3","x**2**3")
    )
)
def test_generateExpression(input, expected):
    assert expressionGenerator.generateExpression(function=input)==expected

def test_generateExpression_empty():
    with pytest.raises(FunctionPlotterException):
        expressionGenerator.generateExpression("")

@pytest.mark.parametrize(
    ("input","expected"),
    (
        ("-x","-x"),
        ("-2","-2"),
        ("-2","-2"),
        ("-5*x+2","-5*x+2"),
        ("-x^2","-x**2")
    )
)
def test_generateExpression_negative_start(input,expected):
    expressionGenerator.generateExpression(input) == expected

@pytest.mark.parametrize(
    ("input"),
    (
        ("/x"),
        ("+x"),
        ("*x"),
        ("^x")
    )
)
def test_generateExpression_illegal_start(input):
    with pytest.raises(FunctionPlotterException):
        expressionGenerator.generateExpression(input)

@pytest.mark.parametrize(
    ("input"),
    (
        ("x x"),
        ("2x"),
        ("-9x5")
    )
)
def test_generateExpression_consecutive_variables(input):
    with pytest.raises(FunctionPlotterException):
        expressionGenerator.generateExpression(input)

@pytest.mark.parametrize(
    ("input"),
    (
        ("x^ ^x"),
        ("x+ +x"),
        ("x/ /x"),
        ("x* *x")
    )
)
def test_generateExpression_consecutive_operators(input):
    with pytest.raises(FunctionPlotterException):
        expressionGenerator.generateExpression(input)

@pytest.mark.parametrize(
    ("input","expected"),
    (
        ("--x","--x"),
        ("---2","---2"),
        ("2--x","2--"),
        ("-5*x+---2","-5*x+--2"),
        ("-x^-----2","-x**-----2")
    )
)
def test_generateExpression_consecutive_negatives(input,expected): #multiple consecutive unary negative operators are allowed
    expressionGenerator.generateExpression(input) == expected

@pytest.mark.parametrize(
    ("input"),
    (
        ("x^2+"),
        ("x^2-"),
        ("x^2*"),
        ("x^2/"),
        ("x^2^")
    )
)
def test_generateExpression_trailing_operators(input):
    with pytest.raises(FunctionPlotterException):
        expressionGenerator.generateExpression(input)