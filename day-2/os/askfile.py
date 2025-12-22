import os


def addnewline(text, length_limit, indlength):
    newtext = ''
    while len(text) > length_limit:
        newtext += text[0:length_limit] + "\n"+ "\t"*indlength
        text = text[length_limit:]
    newtext += text
    return newtext

def prntdirlist(path):
    dirlist = ['.','..'] + os.listdir(path)
    for i, cont in enumerate(dirlist):
        nametype = 'directory' if os.path.isdir(os.path.join(path, cont)) else f'file'
        cont = addnewline(cont, 17, 1)
        print(f'[{i+1}]\t{cont}\t\t\t{nametype}')
    return dirlist


def askfilepath():
    cur_dir = os.getcwd()
    file_path = ''
    while file_path == '':
        os.system('clear')
        print("="*25)
        print(f'{" "*6}select a file{" "*6}')
        print("="*25, '\n')
        print(f'current directory : {cur_dir}\n')
        print('directory content : ')
        dirlist = prntdirlist(cur_dir)
        path_input = input("select with type number or name : ")
        if path_input.isdigit():
            try:
                path_input = int(path_input)
                path_input = os.path.join(cur_dir, dirlist[path_input-1])
                if os.path.isdir(path_input):
                    if os.path.basename(path_input) == '..':
                        path_input = os.path.dirname(cur_dir)
                        cur_dir = path_input
                        continue
                    if os.path.basename(path_input) == '.':
                        path_input = cur_dir
                        cur_dir = path_input
                        continue
                else:
                    file_path = path_input
            except:
                print('out of range, try again!')
        else :
            path_input = os.path.join(cur_dir, path_input)
            if os.path.exists(path_input):
                if os.path.isdir(path_input):
                    if os.path.basename(path_input) == '..':
                        path_input = os.path.dirname(cur_dir)
                        cur_dir = path_input
                        continue
                    if os.path.basename(path_input) == '.':
                        path_input = cur_dir
                        cur_dir = path_input
                        continue
                else:
                    file_path = path_input
            else :
                print(os.path.basename(path_input), "isn't file or directory")

    return file_path

        

file_path = askfilepath()

print('selected file :', file_path)