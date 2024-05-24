class LexicalAnalyzer:
    def __init__(self, syntax):
        self.syntax = syntax

    def __call__(self, *args, **kwargs):
        return args, kwargs
