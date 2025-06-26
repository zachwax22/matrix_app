#type: ignore
import errors
import random

'''
Contains logic for the Matrix class.
All methods for generating and operating on matrices are included here.
'''

class Matrix:
    
    # Magic methods --------------------

    def __init__(self, matrix: str = '', verbose: bool = False) -> None:
        '''
        Basic constructor, initializes an empty 2D matrix (or full if matrix provided)\n
        matrix: string of 2d list to represent matrix, if desired (primarily used for workbook import/export)\n
        verbose: False to hide debug prints (default), True to show them
        '''
        if(type(matrix) == str and len(matrix) > 0):
            # e.g. '[[1, 2, 3], [4, 5, 6], [7, 8, 9]]'
            self._m = []
            rows = matrix.split('], [')
            rows[0] = rows[0][2:]
            rows[-1] = rows[-1][:-2]
            for i in range(len(rows)):
                self._m.append([])
                values = rows[i].split(', ')
                for j in range(len(values)):
                    while(']' in values[j]):
                        values[j] = values[j][:-1]
                    while('[' in values[j]):
                        values[j] = values[j][1:]
                    self._m[i].append(float(values[j]))
                if(self.is_jagged):
                    raise errors.JaggedMatrixError("Given a jagged matrix")
        else:
            self._m = [[]]
        self.verbose = verbose
        self.ecl = 0
        self.ecd = 4

    # The following three magic methods allow the user to interact with the object as if it is the list itself
    # e.g. matrix[0][0] returns the same result as matrix._m[0][0], matrix[3][4] = 2.0 assigns 2.0 to matrix._m[3][4]

    def __getitem__(self, index: int) -> list:
        return self._m[index]

    def __setitem__(self, index: int, value: list) -> None:
        self._m[index] = value
        
    def __len__(self) -> int:
        return len(self._m)

    def __str__(self) -> str: 
        '''Converts the matrix to a legible multi-line string representation.'''
        string_matrix = []
        column_has_negative = []
        for i in range(len(self)): # Converts the matrix to a 2D array of strings - also tracks negatives
            string_matrix.append([])
            for j in range(len(self[i])):
                if(len(column_has_negative) <= j):
                    column_has_negative.append(False)
                self[i][j] = round(self[i][j], 5)
                if(round(self[i][j], 0) == self[i][j]): # Removes redundant '.0's
                    self[i][j] = int(self[i][j])
                if(self[i][j] < 0):
                    column_has_negative[j] = True
                string_matrix[i].append(str(self[i][j]))

        lengths_by_column = [] # Finds the maximum number length in each column
        for i in range(len(string_matrix[0])):
            column = []
            for j in range(len(string_matrix)):
                column.append(len(string_matrix[j][i]))
            lengths_by_column.append(max(column))

        for i in range(len(string_matrix)): # Iterates through each number in the string matrix and adjusts it to that each is height-aligned
            for j in range(len(string_matrix[i])):
                if(column_has_negative[j] and self[i][j] >= 0):
                    string_matrix[i][j] = ' ' + string_matrix[i][j]
                # i: row position, j: column position
                while(len(string_matrix[i][j]) < lengths_by_column[j]):
                    if('.' in string_matrix[i][j]):
                        string_matrix[i][j] += ' '
                    else:
                        string_matrix[i][j] = ' ' + string_matrix[i][j]
        
        result = ''
        for i in range(len(string_matrix)): # Reconstitutes string matrix into lines, then concatenates the lines
            row = ''
            for j in range(len(string_matrix[i])):
                row += string_matrix[i][j] + ' '
            if(i == len(string_matrix) - 1):
                result += row
            else:
                result += row + '\n'

        return result

    __repr__ = __str__

    def __add__(self, other: 'Matrix | float | int')-> 'Matrix':
        '''
        Performs addition for one of two cases:\n
        other is Matrix: adds each element individually if both matrices are of the same dimensions, returns None otherwise\n
        other is num: adds other to each element of the original matrix
        '''
        if(type(other) == Matrix):
            if(len(self) == len(other) and len(self[0]) == len(other[0])):
                result = self.zeroes(len(self), len(self[0]))
                for i in range(len(result)):
                    for j in range(len(result[0])):
                        result[i][j] = self[i][j] + other[i][j]
                return result
            else:
                raise errors.DimensionError("Addition error - incorrect dimensions")
        elif(type(other) == float or type(other) == int):
            result = self.zeroes(len(self), len(self[0]))
            for i in range(len(self)):
                for j in range(len(self[0])):
                    result[i][j] = self[i][j] + other
            return result
        else:
            raise TypeError("Addition error - incorrect type passed")
        
    
    def __sub__(self, other: 'Matrix | float | int') -> 'Matrix':
        '''See __add__.'''
        if(type(other) == Matrix):
            if(len(self) == len(other) and len(self[0]) == len(other[0])):
                result = self.zeroes(len(self), len(self[0]))
                for i in range(len(result)):
                    for j in range(len(result[0])):
                        result[i][j] = self[i][j] - other[i][j]
                return result
            else:
                raise errors.DimensionError("Subtraction error - incorrect dimensions")
        elif(type(other) == float or type(other) == int):
            result = self.zeroes(len(self), len(self[0]))
            for i in range(len(self)):
                for j in range(len(self[0])):
                    result[i][j] = self[i][j] - other
            return result
        else:
            raise TypeError("Subtraction error - incorrect type passed")
            
    def __mul__(self, other: 'Matrix | float | int')-> 'Matrix':
        '''
        Performs multiplication for one of two cases:\n
        other is Matrix: performs matrix multiplication (self must have as many columns as other has rows)\n
        other is num: multiplies each element individually by the given number
        '''
        if(type(other) == float or type(other) == int):
            result = self.zeroes(len(self), len(self[0]))
            for i in range(len(self)):
                for j in range(len(self[0])):
                    result[i][j] = self[i][j] * other
            return result
        elif(type(other) == Matrix):
            if(len(self[0]) == len(other)):
                # dot product case
                if(len(self) == len(other[0]) == 1):
                    result_num = 0.0
                    for i in range(len(self[0])):
                        result_num += self[0][i] * other[i][0]
                    # returns 1x1 matrix instead of float to follow convention
                    result = Matrix()
                    result._m = [[result_num]]
                    return result
                # matrix mult case
                else:
                    result = self.zeroes(len(self), len(other[0]))
                    for i in range(len(result)):
                        for j in range(len(result[0])):
                            # Create two sub-matrices (a row and a column, respectively) to create a dot product
                            A_vec = self.row(i)
                            B_vec = other.column(j)
                            element = A_vec * B_vec # calls the dot product case
                            result[i][j] = element[0][0]
                    return result
            else:
                raise errors.DimensionError("Multiplication error - incorrect dimensions used")
        else:
            raise TypeError("Multiplication error - wrong type used")
            
                
    def __pow__(self, power: int) -> 'Matrix':
        '''Matrix exponentiation for square matrices. All exponents must be ints due to complex numbers being unsupported.'''
        if(type(power) == float and round(power) == power):
            power = int(power)
        if(type(power) == int and self.is_square):
            if(power < 0):
                power = abs(power)
                result = self ** power
                return result.inverse()
            elif(power == 0):
                return self.identity(len(self))
            else:
                result = self.duplicate()
                while(power > 1):
                    result *= self
                    power -= 1
                return result
        elif(type(power) != int):
            raise TypeError("Noninteger power given for exponentiation")
        else:
            raise errors.DimensionError("Exponentiation error - nonsquare matrix given")

    def __abs__(self) -> 'Matrix':
        '''Returns the absolute value of a matrix (i.e. absolute value of each individual element).'''
        result = self.zeroes(len(self), len(self[0]))
        for i in range(len(self)):
            for j in range(len(self[0])):
                result[i][j] = abs(self[i][j])
        return result
    
    def __neg__(self) -> 'Matrix':
        '''Inverts each element in a matrix.'''
        result = self.zeroes(len(self), len(self[0]))
        for i in range(len(self)):
            for j in range(len(self[0])):
                result[i][j] = -self[i][j]
        return result

    def __eq__(self, other: 'Matrix | int | float') -> bool:
        '''Determines equivalency based on the contents of each matrix. Also supports comparing literal numbers (i.e. scalars) and 1x1 matrices.'''
        if(type(other) == Matrix):
            return self._m == other._m
        elif((type(other) == float or type(other) == int) and len(self) == len(self[0]) == 1):
            return self[0][0] == other
        else:
            return False
    
    # Properties    --------------------

    @property
    def is_jagged(self) -> bool:
        '''Determines if a matrix is jagged (i.e. has rows of differing lengths).'''
        for i in range(1, len(self)):
            if(len(self[i]) != len(self[i-1])):
                return True
        return False
    
    @property
    def is_consistent(self) -> bool:
        '''Determines if an (augmented) matrix is consistent - i.e. if it lacks 0=1 cases.'''
        j = len(self) - 1
        if(self[j][-1] == 0):
            return True
        else: # if end value is nonzero, then the rest of the row must have a nonzero
            nonzero_value_present = False
            for i in range(len(self[0]) - 1):
                if(self[j][i] != 0):
                    nonzero_value_present = True
            return nonzero_value_present
        
    @property
    def is_square(self) -> bool:
        '''Determines if a matrix is square (e.g. 2x2, 3x3, etc)'''
        return len(self) == len(self[0])

    # Matrix generators ----------------

    def import_string(self, matrix: str) -> None:
        '''
        Parses user input to create the self._m matrix.
        Accepts MATLAB notation, e.g. [1 2 3; 4.0 -5 6.7; 7 8 9]
        '''
        if(matrix[0] != '['):
            raise errors.ParsingError("Could not parse string")
        else:
            if(matrix[-1] != ']'):
                matrix = matrix[1:matrix.index(']')]
            else:
                matrix = matrix[1:-1] # strips brackets
            rows = matrix.split(';') # splits into rows separated by semicolons
            for i in range(len(rows)):
                rows[i] = rows[i].strip()
                rows[i] = rows[i].split(' ') # splits into numbers separated by whitespace - now a 2d array
                j = 0
                while(j < len(rows[i])):
                    if(rows[i][j] == ''): # if an empty space is given (from extra whitespace), remove it and adjust array accordingly
                        del rows[i][j]
                        j -= 1
                    else:
                        rows[i][j] = float(rows[i][j])
                    j += 1
            self.set(rows)
            if(self.verbose):
                print("String successfully imported as:")
                print(self)

    def set(self, matrix: list[list]):
        if(type(matrix) != list or (len(matrix) > 0 and type(matrix[0] != list))):
            raise TypeError("Given something other than a 2D matrix for set()")
        test_matrix = Matrix()
        test_matrix._m = matrix
        if(test_matrix.is_jagged):
            raise errors.JaggedMatrixError("Given a jagged matrix")
        else:
            self._m = matrix

    def zeroes(self, rows: int, cols: int = -1) -> 'Matrix':
        '''Creates a matrix of zeroes with the specified dimensions. If only one number is provided, a square matrix is created.'''
        if(cols < 0): # square case
            cols = rows
        matrix = Matrix()
        matrix._m = []
        for i in range(rows):
            matrix._m.append([0.0] * cols)
        return matrix
    
    def ones(self, rows: int, cols: int = -1) -> 'Matrix':
        '''Creates a matrix of ones with the specified dimensions. If only one number is provided, a square matrix is created.'''
        if(cols < 0):
            cols = rows
        matrix = Matrix()
        matrix._m = []
        for i in range(rows):
            matrix._m.append([1.0] * cols)
        return matrix

    def identity(self, rows: int, cols: int = -1) -> 'Matrix':
        '''Creates an identity matrix (e.g. [1 0 0; 0 1 0; 0 0 1]) of a given size. If only one number is provided, a square matrix is created.'''
        if(cols < 0): # square case
            cols = rows
        matrix = self.zeroes(rows, cols)
        i = 0
        while(i < len(matrix) and i < len(matrix[0])):
            matrix[i][i] = 1.0
            i += 1
        return matrix

    def randint(self, rows: int, cols: int = -1, start: int = 0, end: int = 255) -> 'Matrix':
        '''
        Creates a matrix of a given size with random numbers from 0 to 255. Mainly used for testing purposes.\n
        start (int=0): inclusive starting number\n
        end (int=255): inclusive ending number
        '''
        if(cols < 0):
            cols = rows
        matrix = self.zeroes(rows, cols)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = random.randint(start, end)
        return matrix

    # Other accesses and operators -----

    def row(self, row: int) -> 'Matrix':
        '''
        Returns a matrix object containing a single row of the given matrix.\n
        row (int): the row to retrieve (row < len(self))
        '''
        if(row < len(self)):
            result = Matrix()
            result[0] =  self[row]
            return result
        else:
            raise errors.RowOutOfBoundsError(f"Row {row} is not in the given matrix")

    def column(self, col: int) -> 'Matrix':
        '''
        Returns a matrix object containing a single column of the given matrix.\n
        col (int): the row to retrieve (col < len(self[0]))
        '''
        if(col < len(self[0])):
            result = Matrix()
            result._m = []
            for i in range(len(self)):
                result._m.append([self[i][col]])
            return result
        else:
            raise errors.ColumnOutOfBoundsError(f"Column {col} is not in the given matrix")

    def slice(self, rows: str, cols: str) -> 'Matrix':
        '''
        Slices a matrix to include only a given row/column range. Follows python syntax.
        To include all rows or columns, make that argument either ':' or ''.\n
        Example:\n
        m._m = [[1,2,3],[4,5,6],[7,8,9]];
        n = m.slice('0:2','2:');
        n._m -> [[3],[6]]
        '''
        (row_start, row_end) = self._slice_parse(rows, False)
        (col_start, col_end) = self._slice_parse(cols, True)
        if(row_start == None or col_start == None):
            raise errors.SliceError("Could not slice matrix")
        result = self._slice_rows(row_start, row_end)
        result = result._slice_columns(col_start, col_end)
        return result
        
    def concat(self, other: 'Matrix') -> 'Matrix':
        '''Concatenates two matrices side-by-side. Matrices must have same number of rows.'''
        if(type(other) == Matrix):
            if(len(self) == len(other)):
                result = self.duplicate()
                for i in range(len(self)):
                    result[i] += other[i]
                return result
            else:
                raise errors.DimensionError("Could not concatenate - matrices had different numbers of rows")
        else:
            raise TypeError("Could not concatenate - wrong type given")
    
    def duplicate(self) -> 'Matrix':
        '''Returns a Matrix object with identical data (no shared memory addresses).'''
        new = Matrix()
        new._m = []
        for i in range(len(self)):
            new._m.append(self[i][:])
        new.verbose = self.verbose
        new.ecl = self.ecl
        new.ecd = self.ecd
        return new

    # Elementary matrix operations -----

    def transpose(self) -> 'Matrix':
        '''Returns the transpose of a given matrix.'''
        result = self.zeroes(len(self[0]), len(self))
        for i in range(len(self)):
            for j in range(len(self[0])):
                result[j][i] = self[i][j]
        return result
    
    def dot(self, other: 'Matrix') -> float:
        '''Takes the dot product of two one-column vectors. To multiply a one-row and one-column matrix, just use the * operator.'''
        if(type(other) == Matrix):
            if(len(self[0]) == len(other[0]) == 1):
                result = 0
                for i in range(len(self)):
                    result += self[i][0] * other[i][0]
                return result
            else:
                raise errors.DimensionError("Wrong dimensions - ensure both vectors are one column each")
        else:
            raise TypeError("Wrong type given for dot product - both must be matrices")

    def determinant(self) -> float:
        '''Computes determinant via cofactor decomposition. Returns None if given an unoperable matrix.'''
        length = len(self)
        if(length != len(self[0]) or length == 0 or self.is_jagged):
            raise errors.DimensionError("Given an uneven, jagged or empty matrix")
        elif(length == 1):
            result = self[0][0]
            if(self.verbose):
                print(f"1x1 matrix - returning {result}")
        elif(length == 2):
            result = self[0][0] * self[1][1] - self[0][1] * self[1][0]
            if(self.verbose):
                print(f"2x2 matrix - returning {result}")
        else:
            result = 0.0
            for i in range(length):
                if(i % 2 == 0):
                    sign = 1
                else:
                    sign = -1
                factor = self[0][i]
                if(factor != 0.0):
                    decomp = self._find_decomposed(i)
                    result += sign * factor * decomp.determinant()
                    if(self.verbose):
                        print(f"Column {i}: Adding {sign} * {factor} * {decomp.determinant()} to result, getting {result}")
        return result

    def row_reduce(self, abort: bool = False) -> 'Matrix':
        '''
        Performs Gauss-Jordan elimination on the matrix.\n
        abort (bool): Aborts early and returns matrix if inconsistency is found (i.e. 0=1), False by default
        '''
        result = self.duplicate()
        if(abort and not self.is_consistent):
            return result
        # step 1 - get to echelon form (upper diagonal only)
        for i in range(len(result[0])):
            if(i < len(result)):
                # initial swap - ensures nonzero pivot
                if(result[i][i] == 0.0):
                    for j in range(i+1, len(result)):
                        if(result[j][i] != 0.0):
                            result._swap(i, j)
                # if pivot is still zero, then column is already cleared at and below the pivot
                if(result[i][i] != 0.0):
                    if(result[i][i] != 1.0):
                        result._scale(i, 1 / result[i][i])
                    for j in range(i+1, len(result)):
                        if(result[j][i] != 0):
                            result._eliminate(j, i, result[j][i])
                            if(abort and not self.is_consistent):
                                return result
        # matrix is now upper triangular
        # the range() below looks weird but it just traverses the list backwards
        for i in range(len(result)-1, -1, -1):
            if(i < len(result[0])):
                for j in range(i-1, -1, -1):
                    if(result[j][i] != 0):
                        result._eliminate(j, i, result[j][i])
                        if(abort and not self.is_consistent):
                            return result
        if(result.ecl >= 1):
            result._round()
        return result
    
    def inverse(self) -> 'Matrix':
        '''Determines the inverse of a given square matrix. Returns None if the matrix is inoperable (i.e. rectangular) or singular.'''
        if(len(self) == len(self[0])):
            compound = self.concat(self.identity(len(self)))
            compound = compound.row_reduce()
            left = compound._slice_columns(0, len(compound[0]) // 2)
            right = compound._slice_columns(len(compound[0]) // 2, len(compound[0]))
            if(left == self.identity(len(self))): # if left half is not the identity matrix, then the given matrix is singular
                return right
            else:
                raise errors.SingularMatrixError("Attempted to invert a singular matrix")
        else:
            raise errors.DimensionError("Given a nonsquare matrix to invert")
        
    # Private methods ------------------

    def _slice_rows(self, start: int, end: int):
        '''
        Slices rows. Start is inclusive and end is exclusive.\n
        start (int): inclusive starting index (0 <= start < len(self))\n
        end (int): exclusive starting index (0 <= end <= len(self))
        '''
        result = self.zeroes(end - start, len(self[0]))
        result._m = []
        while(start < end):
            result._m.append(self[start])
            start += 1
        return result

    def _slice_columns(self, start: int, end: int):
        '''See _slice_rows.'''
        end
        result = self.zeroes(len(self), end - start)
        result._m = []
        for i in range(len(self)):
            result._m.append(self[i][start:end])
        return result

    def _slice_parse(self, txt: str, cols = False) -> tuple:
        '''Parses args received for slice() and yields start/end ints for use in _slice_rows or _slice_columns.'''
        if(txt == '' or txt == ':'):
            start = 0
            if(cols):
                end = len(self[0])
            else:
                end = len(self)
        elif(':' not in txt and txt.isnumeric()):
            start = int(txt)
            end = int(txt) + 1
        else:
            if(txt[0] == ':'):
                start = 0
                end = int(txt[1:])
            elif(txt[-1] == ':'):
                start = int(txt[:-1])
                if(cols):
                    end = len(self[0])
                else:
                    end = len(self)
            else:
                (start, end) = txt.split(':')
                if(start.isnumeric() and end.isnumeric()):
                    (start, end) = (int(start), int(end))
                else:
                    (start, end) = (None, None)

        return (start, end)

    def _find_decomposed(self, working_col: int) -> 'Matrix':
        '''Finds the decomposition of a given matrix, used for determinant algorithm.'''
        decomp = self.zeroes(len(self) - 1)
        i = 0
        decomp_col = 0
        while(i < len(self)):
            if(i == working_col):
                i += 1
            if(i < len(self)):
                for j in range(1, len(self)):
                    decomp[j-1][decomp_col] = self[j][i]
                decomp_col += 1
            i += 1
        if(self.verbose):
            print(f"Decomposition matrix #{working_col}:")
            print(decomp)
        return decomp
    
    def _swap(self, r1: int, r2: int) -> None:
        '''Swaps two rows (generally used for Gauss-Jordan).'''
        if(r1 < len(self) and r2 < len(self)):
            (self[r1], self[r2]) = (self[r2], self[r1])
        if(self.verbose):
            print(f"Swaps rows {r1+1} and {r2+1}, new matrix:")
            print(self)

    def _scale(self, row: int, factor: float | int) -> None:
        '''Scales a row by a given factor (generally used for Gauss-Jordan).'''
        if(row < len(self)):
            for i in range(len(self[row])):
                self[row][i] *= factor
        if(self.verbose):
            print(f"Scales row {row+1} by {factor}, new matrix:")
            print(self)
        if(self.ecl >= 2):
            self._round()

    def _eliminate(self, r1: int, r2: int, factor: float | int) -> None:
        '''Eliminates a number from r1 by subtracting (r2[i] * factor) by itself (generally used for Gauss-Jordan).'''
        if(r1 < len(self) and r2 < len(self)):
            for i in range(len(self[r1])):
                self[r1][i] -= self[r2][i] * factor
        if(self.verbose):
            print(f"Subtracts row {r2+1} * {factor} from row {r1+1}, new matrix:")
            print(self)
        if(self.ecl >= 2):
            self._round()

    def _round(self) -> None:
        '''Accounts for floating-point error by eliminating any decimal values less than 10^-n, with n given by self.ecd.'''
        for i in range(len(self)):
            for j in range(len(self[0])):
                rounded = round(self[i][j], self.ecd)
                if(rounded != self[i][j]):
                    self[i][j] = rounded