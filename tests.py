#type: ignore
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
        self.pass_fail = [0,0]
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
        try:
            result = Matrix('[[1, 2], [3, 4], [5, 6]]') ** 2
        except errors.DimensionError:
            print('Test __pow__ nonsquare passed')
            self.pass_fail[0] += 1
        else:
            print(f'Test __pow__ nonsquare failed \nExpected: \nerrors.DimensionError \nReceived: \n{result}')
            self.pass_fail[1] += 1
        self.test('__pow__ ^1', generic, generic ** 1)
        self.test('__pow__ ^0', generic.identity(3), generic ** 0)
        self.test('__pow__ ^-2', Matrix('[[8.5, -6.0], [-12.0, 8.5]]'), Matrix('[[4, 3], [6, 4]]') ** -2)
        self.test('__abs__', Matrix('[[1, 1], [1, 1]]'), abs(Matrix('[[1, -1], [-1, 1]]')))
        self.test('__neg__', Matrix('[[1, -1], [-1, 1]]'), -Matrix('[[-1, 1], [1, -1]]'))
        self.test('__eq__ true', True, Matrix('[[4, 3], [2, 4]]') == Matrix('[[4, 3], [2, 4]]'))
        self.test('__eq__ false', False, Matrix('[[4, 3], [2, 4]]') == Matrix('[[4, 3], [2, 4], [5, 6]]'))
        self.test('__eq__ num', True, Matrix('[[4]]') == 4)
        self.test('is_consistent false', False, Matrix('[[1, 2, 0, 1], [0, 0, 0, 1]]').is_consistent)
        self.test('is_consistent true', True, Matrix('[[1, 2, 0, 1], [0, 0, 0, 0]]').is_consistent)
        self.test('is_square true', True, generic.is_square)
        self.test('is_square false', False, generic.slice('0:1',':').is_square)
        self.test('is_square empty', True, Matrix().is_square)
        temp = Matrix()
        temp.import_string('[1 2 3; 4 5 6; 7 8 9]')
        self.test('import_string 1', generic, temp)
        temp.import_string('[1 2 3; 4.0 -5 6.7; 7 8 9]')
        self.test('import_string 2', Matrix('[[1, 2, 3], [4, -5, 6.7], [7, 8, 9]]'), temp)
        try:
            temp.import_string('[1 2 3; 4 5]')
        except errors.JaggedMatrixError:
            print('Test import_string 3 passed')
            self.pass_fail[0] += 1
        else:
            print(f'Test import_string 3 failed \nExpected: \nerrors.JaggedMatrixError \nReceived: \n{temp}')
            self.pass_fail[1] += 1
        self.test('zeroes square', Matrix('[[0, 0], [0, 0]]'), temp.zeroes(2))
        self.test('zeroes nonsquare', Matrix('[[0, 0], [0, 0], [0, 0]]'), temp.zeroes(3, 2))
        self.test('ones square', Matrix('[[1, 1], [1, 1]]'), temp.ones(2))
        self.test('ones nonsquare', Matrix('[[1, 1], [1, 1], [1, 1]]'), temp.ones(3, 2))
        self.test('identity square', Matrix('[[1, 0], [0, 1]]'), temp.identity(2))
        self.test('identity tall', Matrix('[[1, 0], [0, 1], [0, 0]]'), temp.identity(3, 2))
        self.test('identity long', Matrix('[[1, 0, 0], [0, 1, 0]]'), temp.identity(2, 3))
        self.test('row', Matrix('[[1, 2, 3]]'), generic.row(0))
        self.test('column', Matrix('[[1], [4], [7]]'), generic.column(0))
        self.test('slice 1', generic.slice(':', ':'), generic.slice('0:3', '0:3'))
        self.test('slice 2', Matrix('[[5, 6], [8, 9]]'), generic.slice('1:', '1:'))
        self.test('slice 3', Matrix('[[1, 2], [4, 5]]'), generic.slice(':2', ':2'))
        self.test('slice 4', 8, generic.slice('2:3', '1:2'))
        self.test('concat', Matrix('[[1, 2, 3, 1, 0, 0], [4, 5, 6, 0, 1, 0], [7, 8, 9, 0, 0, 1]]'), generic.concat(generic.identity(3)))
        try:
            result = generic.concat(generic.zeroes(4))
        except errors.DimensionError:
            print('Test concat 2 passed')
            self.pass_fail[0] += 1
        else:
            print(f'Test concat 2 failed \nExpected: \nerrors.DimensionError \nReceived: \n{result}')
            self.pass_fail[1] += 1
        self.test('duplicate empty', Matrix(), Matrix().duplicate())
        self.test('duplicate', Matrix('[[1, 2, 3], [4, 5, 6], [7, 8, 9]]'), generic.duplicate())
        self.test('transpose square', Matrix('[[1, 4, 7], [2, 5, 8], [3, 6, 9]]'), generic.transpose())
        temp = Matrix('[[1], [2], [3]]')
        self.test('dot', 14.0, temp.dot(temp.duplicate()))
        self.test('determinant zero', 0.0, generic.determinant())
        temp = generic.duplicate()
        temp[2][2] = 7.0
        self.test('determinant nonzero', 6.0, temp.determinant())
        self.test('row_reduce square', Matrix('[[1, 0, -1], [0, 1, 2], [0, 0, 0]]'), generic.row_reduce())
        temp = generic.concat(Matrix('[[6], [3], [1]]'))
        self.test('row_reduce inconsistent w/ abort', Matrix('[[1, 2, 3, 6], [0, 1, 2, 7], [0, 0, 0, 1]]'), temp.row_reduce(True))
        self.test('row_reduce inconsistent w/o abort', Matrix('[[1, 0, -1, -7], [0, 1, 2, 5], [0, 0, 0, 1]]'), temp.row_reduce())
        print(f"{self.pass_fail[0]} tests passed, {self.pass_fail[1]} tests failed")

    def workbook_test(self) -> None:
        self.pass_fail = [0,0]
        wb = Workbook()
        wb.add('val1', 3.0)
        wb['mat1'] = Matrix('[[1, 2], [3, 4]]')
        temp = wb.duplicate()
        wb['mat2'] = wb['mat1'] * wb['val1']
        self.test('workbook basic function', Matrix('[[3, 6], [9, 12]]'), wb['mat2'])
        new_wb = wb.duplicate()
        del new_wb['mat3']
        self.test('__delitem__ DNE', wb, new_wb)
        new_wb.remove('mat2')
        self.test('__eq__ and remove', temp, new_wb)
        repr_example = 'val1^3.0\nmat1|[[1.0, 2.0], [3.0, 4.0]]'
        self.test('repr', repr_example, repr(temp))
        wb.clear()
        repr_example_lst = repr_example.split('\n')
        wb.parse_lines(repr_example_lst)
        self.test('parse_lines', temp, wb)
        print(f"{self.pass_fail[0]} tests passed, {self.pass_fail[1]} tests failed")
