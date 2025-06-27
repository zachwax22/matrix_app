#type: ignore
from matrix import Matrix
from workbook import Workbook

'''Contains the actual user shell'''
def _is_variable(token: str) -> bool:
    ALLOWED_SYMBOLS = ['-','_',"'"]
    if(' ' not in token):
        for i in range(len(token)):
            if(not token[i].isalnum() and token[i] not in ALLOWED_SYMBOLS):
                return False
        return True
    else:
        return False
    
def _is_operator(token: str) -> bool:
    OPERATORS = ['+', '-', '/', '*', '^', '%', '//', '=', '==', '+=', '-=', '*=', '/=', '^=', '%=', '//=']
    return token in OPERATORS
        
    
def main():
    wb1 = Workbook('WB1')
    workbook = wb1
    user_input = input(f'[{workbook.name}] ~$ ')
    while(user_input.lower() not in ("stop", "exit", "quit", ":q", "exit()", "return")):
        '''
        actual shell logic under construction
        outline:
        1) categorize user input (print, assignment, arithmetic, function call, etc)
        2) create subprocesses to parse each of these
        3) direct input to given subprocess and handle from there
        '''
        user_input = input(f'[{workbook.name}] ~$ ')


if(__name__ == "__main__"):
    main()