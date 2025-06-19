# type: ignore
from matrix import Matrix

'''
Contains logic for the Workbook class.
Allows Matrix and scalar objects to be grouped within a workspace, and allows workspaces to be imported and exported via files.
'''

class Workbook:
    def __init__(self, name: str = 'WB1'):
        self.d = {}
        self.name = name
    
    def __getitem__(self, key: str) -> Matrix | float | int:
        return self.d[key]
    
    def __setitem__(self, key: str, value: Matrix | float | int):
        if(type(value) in (Matrix, float, int)):
            self.d[key] = value

    def __delitem__(self, key: str):
        del self.d[key]

    def __len__(self) -> int:
        return len(self.d)
    
    def __str__(self) -> str:
        result = f"Workbook {self.name} containing {len(self)} items:"
        for key, value in self.d.items():
            if(type(value) == Matrix):
                result += f"\n{key}: {len(value)}x{len(value[0])} matrix"
            else:
                result += f"\n{key}: {value} scalar"
        return result
    
    __repr__ = __str__

    def rawdata(self) -> str:
        '''Creates raw workbook data to be exported to file'''
        result = ''
        for key, value in self.d.items():
            if(result != ''):
                result += '\n'
            result += key
            if(type(value) == Matrix):
                result += '|' + str(value.m)
            elif(type(value) == float or type(value) == int):
                result += '^' + str(value)
        return result

    
    def add(self, name: str, matrix: Matrix | float | int) -> None:
        self[name] = matrix

    def remove(self, name: str) -> None:
        del self.d[name]

    def wb_import(self, filepath: str) -> None:
        '''Imports workbook data from a file'''
        file = open(filepath, 'r')
        lines = file.readlines()
        file.close()
        for i in range(len(lines)):
            if('|' in lines[i]):
                (key, value) = lines[i].split('|')
                self[key] = Matrix(value)
            elif('^' in lines[i]):
                (key, value) = lines[i].split('^')
                self[key] = float(value)

    def wb_export(self, filepath: str) -> str:
        '''Creates a file with the workbook data'''
        file = open(filepath, 'w')
        file.write(self.rawdata())
        file.close()
