#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
from urllib.parse import urlparse
from socket import gethostbyname
import re
from requests import get
from numpy import array, log
from pyquery import PyQuery
from string import punctuation

#Content Based Feature Functions
#get_ip
def url_host_is_ip(url):
    host = urlparse(url).netloc
    pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    match = pattern.match(host)
    return match is not None

def get_ip(url):
    parsed_url = urlparse(url)
    try:
        if url_host_is_ip(url):
            ip = parsed_url.netloc
        else :
            ip = gethostbyname(parsed_url.netloc)
        return ip
    except Exception as e:
        return ""
    
def get_html_page(url):
    print(url)
    try:
        html = get(url, timeout = 5)
        if html is not None:
            html = html.text
        else:
            html = ""
    except:
        html = ""
    # print("***",html)
    return html

#Page_Entropy
def get_entropy(text):
    text = text.lower()
    probs = [text.count(c) / len(text) for c in set(text)]
    return -sum([p * log(p) / log(2.0) for p in probs])

#get the number of script tags
def get_pyquery(html):
    try:
        if html is not None:
            pq = PyQuery(html)
        else:
            pq = None
    except:
        pq = None
    return pq

def get_scripts(pq):
    #print("dadas")
    #print(pq('script').text)
    if pq is not None: 
        scripts = pq('script')  
    else: 
        scripts = None
    return scripts

def number_of_script_tags(html):
    pq = get_pyquery(html)
    scripts = get_scripts(pq)
    #print(scripts)
    return len(scripts) if scripts else 0

#script_to_body_ratio
def script_to_body_ratio(html):
    pq = get_pyquery(html)
    scripts = get_scripts(pq)
    if scripts is not None:
        scripts = scripts.text()
        return len(scripts)/length_of_html(html)
    else:
        return 0

def length_of_html(html):
    return len(html)

#number of tokens
def number_of_page_tokens(html):
    html_tokens = len(html.lower().split()) if html else 0
    return html_tokens

#numberof sentences, number of punctuations and number of capitalizations
def number_of_sentences(html):
    html_sentences = len(html.split('.')) if html else 0
    return html_sentences

def number_of_punctuations(html):
    excepts = ['<', '>', '/']
    matches = [i for i in html if i in punctuation and i not in excepts]
    return len(matches)

def number_of_capitalizations(html):
    uppercases = [i for i in html if i.isupper()]
    return len(uppercases)

#find the average number of tokens in sentence
def average_number_of_tokens_in_sentence(html):
        html_sentences = html.split('.')
        sen_lens = [len(i.split()) for i in html_sentences]
        return sum(sen_lens)/len(sen_lens)
    
#get the number of html tags
def number_of_html_tags(html):
    pq = get_pyquery(html)
    return len(pq('*')) if pq else 0

# get the number of hidden tags
def number_of_hidden_tags(html):
    pq = get_pyquery(html)
    if pq is None:
        return 0
    hidden1, hidden2 = pq('.hidden'), pq('#hidden')
    hidden3, hidden4 = pq('*[visibility="none"]'), pq('*[display="none"]')
    hidden = hidden1 + hidden2 + hidden3 + hidden4
    return len(hidden)

#get the number of iframes
def number_of_iframes(html):
    pq = get_pyquery(html)
    if pq is None:
        return 0
    iframes = pq('iframe') + pq('frame')
    return len(iframes)

# get the number of objects
def number_of_objects(html):
    pq = get_pyquery(html)
    if pq is None:
        return 0
    objects = pq('object')
    return len(objects)

# get the number of embeds
def number_of_embeds(html):
    pq = get_pyquery(html)
    if pq is None:
        return 0
    objects = pq('embed')
    return len(objects)

# ge the number of hyperlinls
def number_of_hyperlinks(html):
    pq = get_pyquery(html)
    if pq is None:
        return 0
    hyperlinks = pq('a')
    return len(hyperlinks)

#get the number of whitespaces
def number_of_whitespaces(html):
    whitespaces = [i for i in html if i == ' ']
    return len(whitespaces)

#get the number of included elements
def number_of_included_elements(html):
    pq = get_pyquery(html)
    if pq is None:
        return 0
    toi = pq('script') + pq('iframe') + pq('frame') + pq('embed') + pq('form') + pq('object')
    toi = [tag.attr('src') for tag in toi.items()]
    return len([i for i in toi if i])

#get the number suspicious elements
valid_tags = ['<a>', '<body>', '<button>', '<canvas>', '<center>', '<code>', '<data>', '<div>', '<font>', '<footer>', '<form>', '<frame>'
             '<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<head>', '<header>', '<html>', '<input>', '<img>', '<label>', '<legend>',
             '<li>', '<link>', '<p>', '<source>', '<span>', '<strong>', '<style>', '<table>', '<tr>', '<tbody>', '<th>', '<td>', '<ul>']
def number_of_suspicious_elements(html):
    pq = get_pyquery(html)
    if pq is None:
        return 0
    all_tags = [i.tag for i in pq('*')]
    suspicious = [i for i in all_tags if i not in valid_tags]
    return len(suspicious)

#get the number of double documents
def number_of_double_documents(html):
    pq = get_pyquery(html)
    if pq is None:
        return 0
    tags = pq('html') + pq('body') + pq('title')
    return len(tags) - 3

#get the number of eval functions
def number_of_eval_functions(html):
    pq = get_pyquery(html)
    if pq is None:
        return 0
    scripts = pq('script')
    scripts = ['eval' in script.text().lower() for script in scripts.items()]
    return sum(scripts)

#get the average length of the scripts
def average_script_length(html):
    pq = get_pyquery(html)
    if pq is None:
        return 0
    scripts = pq('script')
    scripts = [len(script.text()) for script in scripts.items()]
    l = len(scripts)
    if l > 0:
        return sum(scripts) / l
    else:
        return 0
    
#get the average script entropy
def average_script_entropy(html):
    pq = get_pyquery(html)
    if pq is None:
        return 0
    scripts = pq('script')
    scripts = [get_entropy(script.text()) for script in scripts.items()]
    l = len(scripts)
    if l > 0:
        return sum(scripts) / l
    else:
        return 0
    
# get the total number of suspicious functions
def number_of_suspicious_functions(html):
    sf = ['eval', 'escape', 'link', 'unescape', 'exec', 'search']
    pq = get_pyquery(html)
    if pq is None:
        return 0
    script_content = pq('script').text()
    susf = [1 if i in script_content else 0 for i in sf]
    return sum(susf)

