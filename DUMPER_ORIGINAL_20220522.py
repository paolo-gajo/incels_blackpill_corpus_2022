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

file_list = filedialog.askopenfilenames(parent=root, title='Choose files to dump')
print(file_list)
i=len(file_list[0])-1
print(i)
slash_n=0
pos1=0
while i>0:
    if file_list[0][i]=='/' and slash_n==0:
        dump_file = file_list[0][:i]
        slash_n+=1
        pos1=i
        i-=1
    if file_list[0][i] == '/' and slash_n == 1:
        dump_file += file_list[0][i:pos1]+'.txt'
        break
    i-=1
print(dump_file)


for file_path in file_list:
    f = open(file_path, 'r', encoding="utf8")
    srt_dump = f.readlines()
    #print(type(srt_dump))
    f.close()
    print(file_path)
    print('number of lines in the file:', len(srt_dump))

    g = open(dump_file, 'a', encoding="utf8")
    for v in srt_dump:
        g.write(v)
    g.close()
