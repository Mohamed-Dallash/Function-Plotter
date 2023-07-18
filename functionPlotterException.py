class FunctionPlotterException(Exception):
     def __init__(self, type, message):
        self.type = type
        self.message = message
        super().__init__(self.message)