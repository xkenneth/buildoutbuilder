class BuildoutBuilderException(Exception):
    def __init__(self, value):
        self.message = 'Exception: '
        self.parameter = value
    def __str__(self):
        return repr(self.message)+repr(self.parameter)

class PartIsNotRecipe(BuildoutBuilderException):
    message = 'Part does not have a recipe:'   

class MissingPart(BuildoutBuilderException):
    message = 'A part is missing:'
