#type: ignore
from matrix import Matrix
from workbook import Workbook

''' Contains the actual user shell
    NOTE: This section of the project is currently mothballed.
    My next semester is about to start, the library works just fine with the interpreter, and I'd be spending a lot of time on something I have little use for.
    '''

def _is_variable(token: str) -> bool:
    '''Determines whether a string token represents a valid variable name'''
    ALLOWED_SYMBOLS = ['-','_',"'"]
    if(' ' not in token):
        for i in range(len(token)):
            if(not token[i].isalnum() and token[i] not in ALLOWED_SYMBOLS):
                return False
        return True
    else:
        return False
    
def _is_operator(token: str) -> bool:
    '''Determines whether a string token represents a valid operator'''
    OPERATORS = ['+', '-', '/', '*', '^', '%', '//', '=', '==', '+=', '-=', '*=', '/=', '^=', '%=', '//=']
    return token in OPERATORS
        
def evaluate(tokens: list):
    pass
    
def main():
    wb1 = Workbook('WB1')
    workbook = wb1
    user_input = input(f'[{workbook.name}] ~$ ').strip()
    while(user_input.lower() not in ("stop", "exit", "quit", ":q", "exit()", "return")):
        '''
        actual shell logic under construction
        outline:
        1) categorize user input (print, assignment, arithmetic, function call, etc)
        2) create subprocesses to parse each of these
        3) direct input to given subprocess and handle from there
        '''
        tokens = user_input.split(' ')
        # print case
        if(len(tokens) == 1 and _is_variable(tokens[0])):
            try:
                print(str(workbook[tokens[0]]))
            except KeyError:
                print("Variable not found")
        # assignment case
        elif(len(tokens) > 3 and _is_variable(tokens[0]) and tokens[1] == '='):
            output = tokens[0]
            tokens = tokens[2:]
        else: # evaluate rest of case, but print to stdout
            output = 'STDOUT'
        # further eval from here
        # determine whether outer call is arithmetic or function, break down tokens further from there

        user_input = input(f'[{workbook.name}] ~$ ').strip()


if(__name__ == "__main__"):
    main()