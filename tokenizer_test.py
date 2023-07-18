import pytest
from tokenizer import Tokenizer
from functionPlotterException import FunctionPlotterException

tokenizer = Tokenizer()

@pytest.mark.parametrize(
    ("input", "expected"),
    (
        ("1",True),
        ("1.1",True),
        ("x",False)
    )
)
def test_isNumeric(input, expected):
    assert tokenizer.isNumeric(input)==expected

def test_tokenize_1():
    tokens,types = tokenizer.tokenize("x^2")
    assert tokens == ['x','^','2']
    assert types == ['var','operator','number']

def test_tokenize_2():
    tokens,types = tokenizer.tokenize("x^2+2*x-3/x")
    assert tokens == ['x','^','2','+','2','*','x','-','3','/','x']
    assert types == ['var','operator','number','operator','number','operator','var','negative','number','operator','var']

def test_tokenize_illegal_variable_name():
    with pytest.raises(FunctionPlotterException):
        tokenizer.tokenize("x+z")

def test_tokenize_illegal_decimal_point():
    with pytest.raises(FunctionPlotterException):
        tokenizer.tokenize(".2*x")

def test_tokenize_multiple_decimal_points():
    with pytest.raises(FunctionPlotterException):
        tokenizer.tokenize("2.0.0*x")

def test_tokenize_illegal_character():
    with pytest.raises(FunctionPlotterException):
        tokenizer.tokenize("x^2+2*(x-3)")