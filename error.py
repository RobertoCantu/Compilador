class RuntimeError(Exception):
    def __init__(self, message):
        super().__init__(message)

class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(message)
    