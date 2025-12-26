import os
from pathlib import Path
from datetime import datetime


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')



def fitit(text, length = 40, indt = 0, space = 0):
    p = 0
    output = ''
    while len(text[p:]) >= length :
        output = output + text[p:p+length] + '\n' + '\t'*indt + ' '* space
        p += length
    return output + text[p:]

def shortit(text, length, red=3, dot=3):
    if len(text) >= length :
        return text[0:length-red] + '.'*dot
    else:
        return text

def fllspc(text, max_length):
    return text + " "*(max_length-len(text))

def unitsize(size):
    units = 'KMGTPEZY'
    exp = -1
    while size//1024 > 0:
        size /= 1024
        exp += 1
    return f'{size:.2f} B' if exp==-1 else f'{size:.2f} {units[exp]}B'

def askfilepath():
    cur_path = Path.cwd()
    width = 77
    selected_path = ''
    while selected_path == '':
        clear()
        title = 'select a file'
        header = ("="*width) + '\n' + f'{" "*((width-len(title))//2)}{title}{" "*((width-len(title))//2)}' + '\n' + ("="*width) + '\n'
        print(header)
        print(f'curent directory : {cur_path.name}')
        print(f'path\t\t : {fitit(str(cur_path), length = 58, indt = 2, space=3)}\n')

        print(f'Index\t| Name\t\t\t| Type\t| Size\t\t| Last Modified')
        print('-'*width)

        dircont = [x for x in cur_path.iterdir()]
        dirprop = [[x.stem, 'dir' if x.is_dir() else ('file' if not x.suffix else x.suffix[1:]), x.stat(), x.name] for x in dircont]

        for i, content in enumerate(dirprop):
            index, name, nametype, last_modified= shortit(str(i+1),5), fllspc(shortit(content[0], 22), 22), shortit(content[1], 4, 0, 0), datetime.fromtimestamp(int(content[2].st_mtime))
            size = ' '*8 if nametype=='dir' else unitsize(content[2].st_size)
            line_content = f'{index}\t| {name}| {nametype}\t|{size}\t| {last_modified}'
            print(line_content)

        path_input = input('\ntype "..", ".", index or name of file or directory : ')

        if path_input.isdigit():
            try:
                path_input = int(path_input) - 1
                path_input = dirprop[path_input]
                if path_input[1] == 'dir':
                    cur_path = cur_path.joinpath(path_input[3])
                    continue
                else :
                    selected_path = str(cur_path.joinpath(path_input[3]))
            except:
                continue
        else:
            if path_input in ['..', '.']:
                cur_path = cur_path.joinpath(path_input).resolve()
            else:
                for prop in dirprop:
                    if path_input in [prop[0], prop[3]]:
                        if prop[1] == 'dir':
                            cur_path = cur_path.joinpath(prop[3]).resolve()
                        else:
                            selected_path = cur_path.joinpath(prop[3]).resolve()

    return selected_path

    
file_path = askfilepath()
print('selected_path :', file_path)
