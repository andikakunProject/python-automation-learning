import csv
from askfile2 import SelectMode, ask_path
from tabulate import tabulate

path = ask_path(SelectMode.FILE, ('csv',))

with open(path, newline="") as csv_file :
    csv_data = csv.reader(csv_file)
    total = 1
    for i, row in enumerate(csv_data):
        if i > total:
            break
        print(row)
        