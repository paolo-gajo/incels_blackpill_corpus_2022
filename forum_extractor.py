import re
import requests
from forum_extractor_functions import escape_remover, html_remover
import urllib.request
from pathlib import Path
import cloudscraper
cloud_session = requests.session()
scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False},sess=cloud_session)

forum_page_counter=1
forum_page_counter_0=forum_page_counter
max_forum_pages=2
markers=True
if markers:
    path_name='bp_markers_'+str(forum_page_counter)+'_'+str(max_forum_pages) #name of the directory im putting the pages in
else:
    path_name = 'bp_no_markers_' + str(forum_page_counter) + '_' + str(max_forum_pages)  # name of the directory im putting the pages in
Path(path_name).mkdir(parents=True, exist_ok=True)

# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0','Cookie': 'xf_notice_dismiss=-1; cf_clearance=9LbLAz9ulCSGh_gsNn4UM_ceCb6NClEpUvsJ0w8UfM8-1653126084-0-150; xf_csrf=IEOdOHTAPqyvQCPx'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0','Cookie': 'xf_notice_dismiss=-1; cf_clearance=9LbLAz9ulCSGh_gsNn4UM_ceCb6NClEpUvsJ0w8UfM8-1653126084-0-150; xf_csrf=IEOdOHTAPqyvQCPx'}
print(headers)
session = requests.Session()
thread_url_list=[]
if forum_page_counter==1:
    url_forum='https://incels.is/forums/inceldom-discussion.2/?prefix_id=1&order=reply_count&direction=desc'
    response_forum=session.get(url_forum,headers=headers) #download first page of the forum
    response_forum_content=str(response_forum.content)
    thread_url_positions=re.finditer('<li class="structItem-startDate"><a href="',response_forum_content)
    thread_url_pos_list=[thread_pos.start()+len('<li class="structItem-startDate"><a href="') for thread_pos in thread_url_positions]
    print(thread_url_pos_list)

    for thread_url_pos in thread_url_pos_list:
        j=0
        thread_url=''
        while response_forum_content[thread_url_pos+j]!='"':
            thread_url+=response_forum_content[thread_url_pos+j]
            j+=1
        thread_url='https://incels.is'+thread_url
        #print(thread_url)
        thread_url_list.append(thread_url)
    forum_page_counter+=1
#first page done
if forum_page_counter>1:
    while forum_page_counter<=max_forum_pages:
        url_forum='https://incels.is/forums/inceldom-discussion.2/page-'+str(forum_page_counter)+'?prefix_id=1&order=reply_count&direction=desc'
        print(url_forum)
        response_forum = session.get(url_forum,headers=headers)  # download first page of the forum
        response_forum_content = str(response_forum.content)
        thread_url_positions = re.finditer('<li class="structItem-startDate"><a href="', response_forum_content)
        thread_url_pos_list = [thread_pos.start() + len('<li class="structItem-startDate"><a href="') for thread_pos in thread_url_positions]
        print(thread_url_pos_list)
        for thread_url_pos in thread_url_pos_list:
            j = 0
            thread_url = ''
            while response_forum_content[thread_url_pos + j] != '"':
                thread_url += response_forum_content[thread_url_pos + j]
                j += 1
            thread_url = 'https://incels.is' + thread_url
            # print(thread_url)
            thread_url_list.append(thread_url)
        forum_page_counter+=1
#all pages done?
page_url_list=[]
url_list=[]
k=1
for url in thread_url_list[0:1]:
    url_list_buffer = []
    response_thread = session.get(url,headers=headers)
    content_str=str(response_thread.content)

    max_page_counter_pos=content_str.find('1 of ')
    if content_str[max_page_counter_pos-1]=='n' and max_page_counter_pos!=-1:
        max_page_counter = ''
        i = 0

        while content_str[max_page_counter_pos + len('1 of ') + i] != '\\':
            max_page_counter += content_str[max_page_counter_pos + len('1 of ') + i]
            i += 1
        print('Got URL for thread #', k)

    else:
        max_page_counter = '1'
        print('Got URL for thread #', k)
    k += 1

    mpc_int=int(max_page_counter)
    url_descr=url[len('https://incels.is/threads/'):]

    for page_thread_counter in range(mpc_int):
        url_list_buffer.append(url+'page-'+str(page_thread_counter+1))
    url_list.append(url_list_buffer)

username_flag=True
content_flag=True
total_post_count=0

a=((forum_page_counter_0-1)*100)
b=0
print(url_list)
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}

for page in url_list:
    thread_content=''
    thread_content_basic=''
    post_number = 1
    for url in page:
        page_content=''
        page_content_basic = ''
        # response_thread = session.get(url,headers=headers)
        response_thread = scraper.get(url).text
        # content_str=str(response_thread.content)
        content_str=str(response_thread)

        if username_flag:
            #find username position
            user_positions_start = re.finditer('data-author="', content_str)
            user_pos_start_list = [user_pos_1.start() + len('data-author="') for user_pos_1 in user_positions_start]
            if 'xfes_similar_threads' in content_str:
                similar_pos=content_str.find('xfes_similar_threads')
                i=0
                similar_count=0
                while i<len(content_str):
                    try:
                        if content_str[similar_pos+i:similar_pos+i+len('xfes_similar_threads')]=='xfes_similar_threads':
                            similar_count+=1
                    except IndexError:
                        break
                    i+=1
                user_pos_start_list = user_pos_start_list[:len(user_pos_start_list)-similar_count]
            # post_pos_end_list = [post_pos_2.start() + len('</article>') for post_pos_2 in post_positions_end]
            user_pos_end_list = []
            for user_pos in user_pos_start_list:
                l = 0
                while content_str[l + user_pos:l + user_pos + len('"')] != '"':
                    l += 1
                user_pos_end_list.append(l + user_pos)
        if content_flag:
            #find content position
            post_positions_start = re.finditer('<article class="message-body js-selectToQuote">', content_str)
            post_pos_start_list = [post_pos_1.start() + len('<article class="message-body js-selectToQuote">') for post_pos_1 in post_positions_start]

            #post_pos_end_list = [post_pos_2.start() + len('</article>') for post_pos_2 in post_positions_end]
            post_pos_end_list=[]
            for pos in post_pos_start_list:
                l=0
                while content_str[l+pos:l+pos+len('</article>')]!='</article>':
                    l+=1
                post_pos_end_list.append(l+pos)

        for i in range(len(post_pos_start_list)):
            if username_flag:
                username=content_str[user_pos_start_list[i]:user_pos_end_list[i]]
                page_content += username + '\t'
            if content_flag:
                post_content_raw=content_str[post_pos_start_list[i]:post_pos_end_list[i]]+ ' ||| '
                print('Post #:',post_number,'URL:',url)
                post_number+=1
                post_content_clean=escape_remover(post_content_raw)
                post_content_no_html=html_remover(post_content_clean)
                page_content+=post_content_no_html
                page_content_basic += post_content_no_html + '\n'
                if username_flag:
                    page_content+='\n'

            total_post_count+=1
        b+=1
        thread_content+=page_content
        thread_content_basic+=page_content_basic
    f = open(path_name + '/thread-' + str(a)+'_'+url[len('https://incels.is/threads/'):len(url)-7]+'.txt', 'w', encoding='utf8')
    if username_flag:
        f.write(page[0]+'\n')
    f.write(thread_content)
    f.close()
    g = open(path_name + '/basic_thread-' + str(a)+'_'+url[len('https://incels.is/threads/'):len(url)-7]+'.txt', 'w', encoding='utf8')
    g.write(thread_content_basic)
    g.close()
    a+=1
    h=open(path_name + '/'+path_name+'_total_post_count'+'.txt', 'w', encoding='utf8')
    h.write(str(total_post_count))
    h.close()

print(total_post_count)