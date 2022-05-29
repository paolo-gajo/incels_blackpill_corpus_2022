from forum_extractor_functions import unique
import re
import tkinter as tk
from tkinter import filedialog

import tkinter as tk
import tkinter.filedialog as fd
from pathlib import Path

from datetime import date

today = date.today()

root = tk.Tk()
# lemma_path = filedialog.askopenfilename(parent=root, title='Choose lemma list file')
lemma_path='bp_100_keywords_python_search.txt'
term_list=[]
term_lemma=[]
i=0
f=open(lemma_path,'r',encoding='utf8')
with open(lemma_path) as f:
    term_list=f.read().splitlines()#.split(',')
    for term in term_list:
        buffer=term_list[i]
        buffer2=buffer.split('\t')
        term_list[i]=buffer2
        i+=1
f.close()
print(term_list)
corpus_path = filedialog.askopenfilename(parent=root, title='Choose corpus file')
# corpus_path='bp_01_100_w_usernames_delimited_w_links.txt'
# corpus_path='foids_test_short.txt'
# corpus_path='foids_test.txt'

# g=open('bp_1_20_128601/bp_1_20_128601_subset_1M.txt','r',encoding='utf8')
g=open(corpus_path,'r',encoding='utf8')
corpus_w_usernames=g.readlines()
g.close()
# corpus_w_usernames=[line.split() for line in corpus_w_usernames] #as a list of lists of words
# corpus_w_usernames=[line for line in corpus_w_usernames] #as a list of strings
print('len(corpus_w_usernames)',len(corpus_w_usernames))
term_count_list=[0 for term in term_list]
username_list=[[] for term in term_list]
lemma_counts={}
for lemma_list in term_list:
    for lemma in lemma_list:
        lemma_counts[lemma]=0
# print(term_count_list)
i=0 #term index
j=0 #line position
k=0 #line number
# term_list=[['females','']]
for lemma_list in term_list:
    print(lemma_list,i+1,'of',len(term_list))
    # if lemma_list[1]=='':
    #     lemma_list=[lemma_list[0]]
    k=0
    for k in range(len(corpus_w_usernames)):
    # for k in range(6000):
        line=corpus_w_usernames[k]
        # print(line)
        line_sum = 0
        found_in_line=0
        username=''
        line=line.lower()
        # line=tokenizer.tokenize(line)
        # print(line)
        if line[0:8] != '\thttps:/':
            j = 0
            while line[j] != '\t':
                username += line[j]
                j += 1
            for lemma in lemma_list:
                line_sum_buffer=sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(lemma), line[j:]))
                lemma_counts[lemma]+=line_sum_buffer
                line_sum+=line_sum_buffer
            term_count_list[i]+=line_sum

            if line_sum and username not in username_list[i]:
                username_list[i].append(username)
        k+=1
            # print(word)
            # print(lemma)
            # j=0
            # if len(lemma.split())==2:
            #     while j<len(line):
            #         try:
            #             if lemma == line[j]+' '+line[j+1]:
            #                 # print('found')
            #                 term_count_list[i]+=1
            #                 # print('line', line[0])
            #                 if line[0] not in username_list:
            #                     username_list[i].append(line[0])
            #                     # print(username_list)
            #         except IndexError:
            #             break
            #         j += 1
            # if len(lemma.split())==3:
            #     while j<len(line):
            #         try:
            #             if lemma == line[j]+' '+line[j+1]+' '+line[j+2]:
            #                 # print('found')
            #                 term_count_list[i]+=1
            #                 # print('line',line[0])
            #                 if line[0] not in username_list:
            #                     username_list[i].append(line[0])
            #                     # print(username_list)
            #         except IndexError:
            #             break
            #         j += 1
            # else:
            #     while j < len(line):
            #         try:
            #             if lemma == line[j]:
            #                 # print('found')
            #                 term_count_list[i] += 1
            #                 # print('line',line[0])
            #                 if line[0] not in username_list:
            #                     username_list[i].append(line[0])
            #                     # print(username_list)
            #         except IndexError:
            #             break
            #         j+=1
    i+=1
# print(username_list)
print('got to this line_number:',k)

# username_unique_list=[]
# i=0
# for list in username_list:
#     # if unique(list)==list:
#     #     print('delete code')
#     if username_list[i]!=unique(list):
#         print('need this after all')
#     unique_list=unique(list)
#     username_unique_list.append(unique_list)
#     i+=1

# print('username_unique_list',username_unique_list[:10])
username_unique_count=[]

for list in username_list:
    username_unique_count.append(len(list))
print('username_unique_count',username_unique_count)
print('term_count_list',term_count_list)
print('lemma_counts',lemma_counts)

d1 = today.strftime('%Y-%m-%d')

# h=open('bp_01_100/bp_01_100_table_casual_tokenizer_females.txt','w',encoding='utf8')
h=open(corpus_path[:len(corpus_path)-4]+'_data_table_'+d1+'.txt','w',encoding='utf8')
h.write('Term'+'\t'+'Occurrences'+'\t'+'Unique users'+'\t'+'Occurrences-posters ratio'+'\n')
i=0
lemma_print=''
for lemma_list in term_list:
    if len(lemma_list)>1:
        j=0
        lemma_print = ''
        for lemma in lemma_list:
            if j==len(lemma_list):
                lemma_print += lemma
            else:
                lemma_print+=lemma+', '
            j+=1
    else:
        lemma_print=lemma_list[0]
    if username_unique_count[i]!=0:
        h.write(lemma_print+'\t'+str(term_count_list[i])+'\t'+str(username_unique_count[i])+'\t'+str(round(term_count_list[i]/username_unique_count[i],2))+'\n')
    else:
        h.write(lemma_print + '\t' + str(term_count_list[i]) + '\t' + str(username_unique_count[i]) + '\t' + 'N/A' + '\n')
    i+=1
h.close()