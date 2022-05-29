def escape_remover(post_content_raw):
    if len(post_content_raw)>=2:
        if post_content_raw[0] == '\\' and post_content_raw[1]=='n':
            post_content_raw=post_content_raw[2:]
            if post_content_raw[0]==' ':
                post_content_raw=post_content_raw[1:]
    post_content_clean=''
    j=0
    while j < len(post_content_raw):
        if post_content_raw[j] == '\\':
            j+=1
            if post_content_raw[j] in 'nt':
                # j+=1
                post_content_clean +=' '
                if j > len(post_content_raw) - 1:
                    j = len(post_content_raw) - 1
            if post_content_raw[j]=='\'':
                post_content_clean+=post_content_raw[j]

        else:
            if j>len(post_content_raw)-1:
                j=len(post_content_raw)-1
            # print(j,len(post_content_raw))
            post_content_clean+=post_content_raw[j]
        j+=1
    post_content_clean = ' '.join(post_content_clean.split())
    return post_content_clean

def html_remover(post_content_clean, j=0):
    post_content_no_html=''
    while j < len(post_content_clean):
        mon=post_content_clean[j]
        if post_content_clean[j] == '<':
            j += 1

            if j == len(post_content_clean):
                break
            mon = post_content_clean[j]
            if post_content_clean[j:j+len('blockquote')]=='blockquote':
                mon = post_content_clean[j]
                while post_content_clean[j:j+len('/blockquote')]!='/blockquote':
                    j+=1
                if post_content_clean[j:j+len('/blockquote')]=='/blockquote':
                    j+=len('/blockquote')
            while post_content_clean[j] != '>':
                j += 1

                if j == len(post_content_clean):
                    break
                mon = post_content_clean[j]
        if post_content_clean[j] == '>':
            j += 1

            if j == len(post_content_clean):
                break
            mon = post_content_clean[j]
        if post_content_clean[j] not in '<>':
            post_content_no_html += post_content_clean[j]
            j += 1
        if j == len(post_content_clean):
            break
        mon = post_content_clean[j]
    post_content_no_html=post_content_no_html.replace('{ "lightbox_close": "Close", "lightbox_next": "Next", "lightbox_previous": "Previous", "lightbox_error": "The requested content cannot be loaded. Please try again later.", "lightbox_start_slideshow": "Start slideshow", "lightbox_stop_slideshow": "Stop slideshow", "lightbox_full_screen": "Full screen", "lightbox_thumbnails": "Thumbnails", "lightbox_download": "Download", "lightbox_share": "Share", "lightbox_zoom": "Zoom", "lightbox_new_window": "New window", "lightbox_toggle_sidebar": "Toggle sidebar" }','')
    post_content_no_html=post_content_no_html.replace('e28099','\'')
    post_content_no_html=post_content_no_html.replace('e2809c', '')
    post_content_no_html=post_content_no_html.replace('e2809d', '')
    post_content_no_html=post_content_no_html.replace('&amp; ', '')
    post_content_no_html=post_content_no_html.replace('&nbsp; ', '')
    post_content_no_html = post_content_no_html.replace('&nbsp;', '')
    post_content_no_html=post_content_no_html.replace('e28094', '')
    post_content_no_html=post_content_no_html.replace('&quot;', '') + ' '
    post_content_no_html=' '.join(post_content_no_html.split())
    post_content_no_html = post_content_no_html.replace('|||', '||| ')
    return post_content_no_html[:len(post_content_no_html)]

def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    return unique_list