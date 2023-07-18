from functionPlotterException import FunctionPlotterException
from tokenizer import Tokenizer

class ExpressionGenerator:
    def generateExpression(self, function):
        tokenizer = Tokenizer()
        tokens,types = tokenizer.tokenize(input_expression=function)
        expression = ""
        state = "start"
        states=[]
        states.append(state)
        i=0
        if not len(tokens):
            raise FunctionPlotterException(type="Syntax Error",message="Function cannot be blank")
        while i < len(types):
            if state == "start":
                if types[i]=="negative":
                    state = "start"
                elif types[i]=="var" or types[i]=="number":
                    state = "complete expression"
                else:
                    raise FunctionPlotterException(type="Syntax Error", message=f"Can't start the function with a {tokens[i]}")
                    
            elif state == "complete expression":
                if types[i] == "negative":
                    state = "incomplete expression"
                elif types[i]=="operator":
                    state = "incomplete expression"
                    if tokens[i]=='^':
                        tokens[i]="**"
                else:
                    raise FunctionPlotterException(type="Syntax Error", message=f"Near the end of {expression}\nExpected an operator between {tokens[i-1]} and {tokens[i]}")
                    
            elif state == "incomplete expression":
                if types[i] == "negative":
                    state = "incomplete expression"
                elif types[i] == "var" or types[i]=="number":
                    state = "complete expression"
                else:
                    raise FunctionPlotterException(type="Syntax Error", message=f"Near the end of {expression}\nExpected a number or variable between {tokens[i-1]} and {tokens[i]}")
            
            expression+=tokens[i]
            i += 1
        if state != "complete expression":
            raise FunctionPlotterException(type="Syntax Error", message=f"Near the end of {expression}\nExpected a number or variable after {tokens[i-1]}")
        return expression