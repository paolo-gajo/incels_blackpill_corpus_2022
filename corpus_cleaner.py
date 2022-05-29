'''
Created on May 16, 2021

@author: paolo
'''
import tkinter as tk
from tkinter import filedialog

import tkinter as tk
import tkinter.filedialog as fd

root = tk.Tk()

#root.withdraw()

file_list = filedialog.askopenfilenames(parent=root, title='Choose files to clean')
# dump_file = filedialog.askopenfilename(parent=root, title='Select or create dump file')

for file_path in file_list:
    f = open(file_path, 'r', encoding="utf8")
    file_content = f.readlines()
    f.close()
