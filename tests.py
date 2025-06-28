from matrix import Matrix
from workbook import Workbook
import errors

class Test:

    pass_fail = [0,0]

    def test(self, id: str, expected, received) -> None:
        if(expected == received):
            print(f"Test {id} passed")
            self.pass_fail[0] += 1
        else:
            print(f"Test {id} failed \nExpected: \n{expected} \nReceived: \n{received}")
            self.pass_fail[1] += 1

    def matrix_test(self) -> None:
        generic = Matrix()
        generic.set([[1.0, 2.0, 3.0],[4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])

        self.test('__init__ 1', generic, Matrix('[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]'))
        try:
            result = Matrix('[[1.0, 2.0, 3.0], [4.0, 5.0], [7.0, 8.0, 9.0]]')
        except errors.JaggedMatrixError:
            print('Test __init__ 2 passed')
            self.pass_fail[0] += 1
        else:
            print(f'Test __init__ 2 failed \nExpected: \nerrors.JaggedMatrixError \nReceived: \n{result}')
            self.pass_fail[1] += 1
        self.test('__repr__', '[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]', repr(generic))
        expected = Matrix()
        expected.set([[2.0, 3.0, 4.0], [5.0, 6.0, 7.0], [8.0, 9.0, 10.0]])
        self.test('__add__ int', expected, generic + 1.0)
        self.test('__sub__', expected, generic - -1)
        self.test('__add__ & __mul__', generic + generic, generic * 2)
        expected.set([[30,36,42],[66,81,96],[102,126,150]])
        self.test('__mul__', expected, generic * generic)
        self.test('__mul__', Matrix('[[9, 12, 15], [24, 33, 42], [39, 54, 69]]'), Matrix('[[1, 2], [4, 5], [7, 8]]') * Matrix('[[1, 2, 3], [4, 5, 6]]'))
        self.test('__pow__', Matrix('[[468, 576, 684], [1062, 1305, 1548], [1656, 2034, 2412]]'), generic ** 3)
        '''
        Full list of tests to cover:
        __pow__:
        ^3, ^30, ^3.0, ^3.5, nonsquare matrix, ^1, ^-2, ^0
        __abs__:
        one case
        __neg__: 
        one case
        __eq__:
        true case, false case, num case
        is_jagged:
        true case, false case, empty case
        is_consistent:
        true case, false case
        is square:
        true case, false case, empty case
        import_string:
        two regular cases, jagged case
        set:
        typeerror case, jagged case, regular case
        zeroes:
        square case, nonsquare case
        ones:
        square case, nonsquare case
        identity:
        square case, nonsquare case
        randint:
        N/A
        row:
        0, len-1, len, -1, len+1
        column:
        0, len[0]-1,len[0], -1, len[0]+1
        slice:
        bounds on both sides, no front bounds, no end bounds, neither, one row/one col
        concat:
        regular case, wrong dimensions case, type error case
        duplicate:
        regular case, empty case
        transpose:
        square case, nonsquare case
        dot:
        regular case, wrong dimensions case, type error case
        determinant:
        regular case, zero case, empty, jagged
        row reduce:
        square case, (n)x(n+1) case, abort early case, (n+1)x(n) case
        inverse:
        two regular cases, singular case, dimension error case
        '''
        print(f"{self.pass_fail[0]} tests passed, {self.pass_fail[1]} tests failed")
