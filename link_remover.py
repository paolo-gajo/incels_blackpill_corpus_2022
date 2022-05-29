import tkinter as tk
from tkinter import filedialog

import tkinter as tk
import tkinter.filedialog as fd
from pathlib import Path



root = tk.Tk()
path = filedialog.askopenfilename(parent=root, title='Choose file')
g=open(path,'r',encoding='utf8')
corpus=g.readlines()
g.close()

f=open(path[:len(path)-4]+'_NO_LINKS.txt','w',encoding='utf8')
for line in corpus:
    if line[0:8] != '\thttps:/':
        f.write(line)
f.close()
