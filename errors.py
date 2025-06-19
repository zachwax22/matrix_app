'''
Errors used throughout the code. ZeroDivisionError and TypeError are also used.
'''

class DimensionError(Exception):
    pass
class ParsingError(Exception):
    pass
class RowOutOfBoundsError(Exception):
    pass
class ColumnOutOfBoundsError(Exception):
    pass
class SliceError(Exception):
    pass
class SingularMatrixError(Exception):
    pass