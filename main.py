#type: ignore
from matrix import Matrix
from workbook import Workbook

'''Contains the actual user shell'''
def _is_variable(token: str) -> bool:
    if(' ' not in token):
        
    
def main():
    wb1 = Workbook('WB1')
    workbook = wb1
    user_input = input(f'[{workbook.name}] ~$ ')
    while(user_input.lower() not in ("stop", "exit", "quit", ":q", "exit()", "return")):
        # do stuff here!
        user_input = input(f'[{workbook.name}] ~$ ')


if(__name__ == "__main__"):
    main()