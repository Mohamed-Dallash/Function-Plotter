from functionPlotterException import FunctionPlotterException
from tokenizer import Tokenizer

class ExpressionGenerator:
    def generateExpression(self, function):
        tokenizer = Tokenizer()
        tokens,types = tokenizer.tokenize(input_expression=function)
        temp_tokens = tokens.copy()
        expression = ""
        temp_expression = expression
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
                    raise FunctionPlotterException(type="Syntax Error", message=f"Near the end of {temp_expression}\nExpected an operator between {temp_tokens[i-1]} and {temp_tokens[i]}")
                    
            elif state == "incomplete expression":
                if types[i] == "negative":
                    state = "incomplete expression"
                elif types[i] == "var" or types[i]=="number":
                    state = "complete expression"
                else:
                    raise FunctionPlotterException(type="Syntax Error", message=f"Near the end of {temp_expression}\nExpected a number or variable between {temp_tokens[i-1]} and {temp_tokens[i]}")
            
            expression+=tokens[i]
            temp_expression+=temp_tokens[i]
            i += 1
        if state != "complete expression":
            raise FunctionPlotterException(type="Syntax Error", message=f"Near the end of {temp_expression}\nExpected a number or variable after {temp_tokens[i-1]}")
        return expression