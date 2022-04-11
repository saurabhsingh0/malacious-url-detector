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

#Lexical Based Feature Functions
def get_entropy(text):
        text = text.lower()
        probs = [text.count(c) / len(text) for c in set(text)]
        entropy = -sum([p * log(p) / log(2.0) for p in probs])
        return entropy
    
def url_string_entropy(url):
        return get_entropy(url)
    
def url_scheme(url):
        # print(url)
        # print(urlparse)
        return urlparse(url).scheme

def url_length(url):
        return len(url)

def url_path_length(url):
        return len(urlparse(url).path)
    
def url_host_length(url):
        return len(urlparse(url).netloc)
    
def url_has_port_in_string(url):
        has_port = urlparse(url).netloc.split(':')
        return len(has_port) > 1 and has_port[-1].isdigit()

def number_of_digits(url):
        digits = [i for i in url if i.isdigit()]
        return len(digits)

def number_of_parameters(url):
        params = urlparse(url).query
        return 0 if params == '' else len(params.split('&'))

def number_of_fragments(url):
        frags = urlparse(url).fragment
        return len(frags.split('#')) - 1 if frags == '' else 0

def is_encoded(url):
        return '%' in url.lower()

def num_encoded_char(url):
        encs = [i for i in url if i == '%']
        return len(encs)

def number_of_subdirectories(url):
        d = urlparse(url).path.split('/')
        return len(d)

def number_of_periods(url):
        periods = [i for i in url if i == '.']
        return len(periods)
    
def has_client_in_string(url):
        return 'client' in url.lower()
    
def has_admin_in_string(url):
        return 'admin' in url.lower()

def has_server_in_string(url):
        return 'server' in url.lower()

def has_login_in_string(url):
        return 'login' in url.lower()

def get_tld(url):
      return urlparse(url).netloc.split('.')[-1].split(':')[0]

