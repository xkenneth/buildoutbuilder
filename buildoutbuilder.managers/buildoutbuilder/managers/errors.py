class BuildoutBuilderException(Exception):
    def __init__(self, value):
        self.message = self.__doc__
        self.parameter = value
    def __str__(self):
        return repr(self.message)+repr(self.parameter)

class PartIsNotRecipe(BuildoutBuilderException):
    """Part does not have a recipe."""

class MissingPart(BuildoutBuilderException):
    """A part is missing."""
    
    
