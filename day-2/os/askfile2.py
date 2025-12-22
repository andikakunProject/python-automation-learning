import os
from pathlib import Path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def askfilepath():
    cur_path = Path.cwd()
    
    clear_screen()
    width = 72
    title = 'select a file'
    header = ("="*width) + '\n' + f'{" "*((width-len(title))//2)}{title}{" "*((width-len(title))//2)}' + '\n' + ("="*width) + '\n'
    print(header)
    print('curent directory :', cur_path)
    
askfilepath()
