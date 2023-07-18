from functionPlotterException import FunctionPlotterException



class Tokenizer:

    def isNumeric(self,num):
        for c in num:
            if not c.isdigit() and not c=='.':
                return False
        return True
    
    def tokenize(self, input_expression):

        operators = ['+', '-', '/', '*', '^']
        white_spaces = ('\n', '\t', ' ')
        tokens = []
        types = []

        i = 0
        state = "start"
        temp_token = ""
        while i < len(input_expression):
            if input_expression[i].isdigit() or input_expression[i].isalpha() or input_expression[i] in white_spaces or input_expression[i] in operators or input_expression[i]=='.':
                if state == "start":
                    if input_expression[i] in white_spaces:
                        state = "start" 
                    elif input_expression[i].isalpha():
                        if(input_expression[i]=='x'):
                            temp_token += input_expression[i]
                            state = "inVar"
                        else:
                            raise FunctionPlotterException(type="Syntax Error", message="Only lowercase x is allowed as a variable name")

                    elif input_expression[i].isdigit() and not input_expression[i]=='.':
                        temp_token += input_expression[i]
                        state = "inNumWhole"
                    
                    elif input_expression[i] in operators:
                        temp_token += input_expression[i]
                        state = "inOperator"
                    else:
                        raise FunctionPlotterException(type="Syntax Error", message="Illegal placement of decimal point")

                elif state == "inVar":
                    state = "done"
                elif state == "inOperator":
                    state = "done"
                elif state == "inNumWhole":
                    if input_expression[i].isdigit():
                        temp_token += input_expression[i]
                        state = "inNumWhole"
                    elif input_expression[i]=='.':
                        temp_token += input_expression[i]
                        state = "inNumFraction"
                    else:
                        state = "done"
                elif state == "inNumFraction":
                    if input_expression[i].isdigit():
                        temp_token += input_expression[i]
                        state = "inNumFraction"
                    elif input_expression[i] == '.':
                        raise FunctionPlotterException(type="Syntax Error", message="Only one decimal point is allowed per number")
                    else:
                        state = "done"
            else:
                raise FunctionPlotterException(type="Syntax Error", message=f"Illegal Character \'{input_expression[i]}\'")
                 
            if state != "done":
                i += 1
            if state == "done":
                tokens.append(temp_token)
                temp_token = ""
                state = "start"
                
        if (state != "start"):
            tokens.append(temp_token)

        for i in tokens:
            if i == "-":
                types.append("negative")
            elif i in operators:
                types.append("operator")
            elif self.isNumeric(i):
                types.append("number")
            elif i == "x":
                types.append("var")
            else:
                raise FunctionPlotterException(type="Syntax Error", message="Error in syntax near the end of the function")
                
        return tokens, types