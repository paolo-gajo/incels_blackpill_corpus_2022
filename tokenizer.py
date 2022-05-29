# from forum_extractor_functions import unique
# from nltk.tokenize import TreebankWordTokenizer
# tokenizer = TreebankWordTokenizer()

# import pyonmttok
# tokenizer = pyonmttok.Tokenizer("conservative", joiner_annotate=True)

# from spacy.tokenizer import Tokenizer
# from spacy.lang.en import English
# nlp = English()
# # Create a blank Tokenizer with just the English vocab
# tokenizer = Tokenizer(nlp.vocab)

from nltk.tokenize import casual_tokenize

import tkinter as tk
from tkinter import filedialog

import tkinter as tk
import tkinter.filedialog as fd
from pathlib import Path



root = tk.Tk()
path = filedialog.askopenfilename(parent=root, title='Choose file to tokenize')
g=open(path,'r',encoding='utf8')
corpus=g.readlines()
g.close()

# print(corpus_w_usernames)
corpus=[line.lower() for line in corpus]
# print(corpus)

username_list=[]
for line in corpus:
    username = ''
    if line[0:5]!='https':
        try:
            j=0
            while line[j]!='\t':
                username+=line[j]
                j+=1
        except IndexError:
            break
    username_list.append(username)
corpus_w_usernames=[]
i=0
print(username_list[:20])

for line in corpus:
    if line[0:5]!='https':
        corpus_w_usernames.append(username_list[i]+line[len(username_list[i]):])
    else:
        corpus_w_usernames.append(line)
    i+=1
print(corpus_w_usernames[:10])
# print(username_list[:10])
corpus_tokenized=[]
monitor=0
# print(type(corpus_w_usernames))
lc=0
for line in corpus_w_usernames:
    # tokens=tokenizer.tokenize(line[len(username_list[lc]):]) #nltk
    # tokens=tokenizer(line[len(username_list[lc]):]) #spacy
    tokens = casual_tokenize(line[len(username_list[lc]):])  # ntlk casual tokenizer
    tokens=[str(token) for token in tokens]
    # print(tokens)
    line_tokenized=' '.join(tokens)
    # print(type(line_tokenized))
    # print('line_tokenized',line_tokenized)
    if line[0:8] != 'https://':
        corpus_tokenized.append(username_list[lc]+'\t'+line_tokenized)
    else:
        corpus_tokenized.append(line_tokenized)
    # print('corpus_tokenized',corpus_tokenized[lc])
    lc+=1
    # print(monitor)
    monitor+=1
# corpus_w_usernames=[' '.join(tokenizer.tokenize(line)) for line in corpus_w_usernames]
# for line in corpus_tokenized[:10]:
#     print('corpus_tokenized line',line)

g=open(path[:len(path)-4]+'_tokenized_casual_tokenizer.txt','w',encoding='utf8')
for line in corpus_tokenized:
    g.write(line+'\n')
    # g.write(line)
g.close()