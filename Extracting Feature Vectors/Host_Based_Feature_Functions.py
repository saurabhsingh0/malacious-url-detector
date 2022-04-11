#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import whois
import waybackpy
from waybackpy import WaybackMachineCDXServerAPI as Cdx
from socket import gethostbyname
import shodan
from socket import socket
# from shodan import Shodan
from requests import get
from urllib.parse import urlparse
from datetime import datetime
from re import compile
from json import dump, loads
from time import sleep
from urllib.parse import urlparse
from socket import gethostbyname
import re

#Host Based Feature Functions
def get_whois_dict(url):
    try:
        whois_dict = whois.whois(url)
        return whois_dict
    except:
        return {}

# print(get_whois_dict(url))

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

def get_shodan_dict(url):
    api = shodan.Shodan('XoeVnzTpSvnUaBKwylwAE9c43TSm3sbl')
    try:
        host = api.host(get_ip(url))
        return host
    except:
        return {}

# print(get_shodan_dict(url))

def parse_before_date(date_string):
    month_year = date_string.split()[-1]
    d = '01-{}'.format(month_year)
    d = datetime.strptime(d, '%d-%b-%Y')
    return d

def parse_whois_date(url, date_key):
    # print(url)
    whois = get_whois_dict(url)
    cdate = whois.get(date_key)
    if cdate:
        if isinstance(cdate, str) and 'before' in cdate:
            d = parse_before_date(cdate)
        elif isinstance(cdate, list):
            d = cdate[0]
        else:
            d = cdate
    return d if cdate else cdate

def get_site_snapshots(url):
    try:
        snapshots = Cdx(urlparse(url).netloc).snapshots()
        snapshots = [snapshot.datetime_timestamp for snapshot in snapshots]
        return snapshots
    except:
        return []

# print(get_site_snapshots(url))

def number_of_subdomains(url):
    whois = get_whois_dict(url)
    shodan = get_shodan_dict(url)
    ln1 = whois.get('nets', None)
    ln2 = shodan.get('domains', None)
    ln = ln1 or ln2
    return len(ln) if ln else None

# print(number_of_subdomains(url))

def url_creation_date(url):
    print(url)
    d = parse_whois_date(url, 'creation_date')
    return d

# print(url_creation_date(url))

def url_expiration_date(url):
    d = parse_whois_date(url, 'expiration_date')
    return d

# print(url_expiration_date(url))

def url_last_updated(url):
    d = parse_whois_date(url, 'updated_date')
    return d

# print(url_last_updated(url))

def url_age(url):
    try:
        days = (datetime.today()-url_creation_date(url)).days
    except:
        days = None
    return days

# print(url_age(url))

def url_intended_life_span(url):
    try:
        lifespan = (url_expiration_date(url)-url_creation_date(url)).days
    except:
        lifespan = None
    return lifespan

# print(url_intended_life_span(url))

def url_life_remaining(url):
    try:
        rem = (url_expiration_date(url)-datetime.today()).days
    except:
        rem = None
    return rem

# print(url_life_remaining(url))

def url_registrar(url):
    d = parse_whois_date(url, 'registrar')
    return d

# print(url_registrar(url))

def url_registration_country(url):
    d = parse_whois_date(url, 'country')
    return d

# print(url_registration_country(url))

def url_host_country(url):
    shodan = get_shodan_dict(url)
    c = shodan.get('country_name', None)
    return c

# print(url_host_country(url))

def url_open_ports(url):
    shodan = get_shodan_dict(url)
    ports = shodan.get('ports', '')
    return ports if ports != '' else None

# print(url_open_ports(url))

def url_num_open_ports(url):
    ports = url_open_ports(url)
    lp = len(ports) if ports else 0
    return lp

# print(url_num_open_ports(url))

def url_is_live(url):
    url = '{}://{}'.format(urlparse(url).scheme, urlparse(url).netloc)
    try:
        return get(url, timeout = 2).status_code == 200
    except:
        return False

# print(url_is_live(url))

def url_isp(url):
    shodan = get_shodan_dict(url)
    return shodan.get('isp', '')

# print(url_isp(url))

def url_connection_speed(url):
    url = '{}://{}'.format(urlparse(url).scheme, urlparse(url).netloc)
    if url_is_live(url):
        return get(url, timeout = 2).elapsed.total_seconds()
    else:
        return None

# print(url_connection_speed(url))

def first_seen(url):
    try:
        fs = snapshots[0]
        return fs
    except:
        return datetime.now()

# print(first_seen(url))

def get_os(url):
    shodan = get_shodan_dict(url)
    oss = shodan.get('os', None)
    return oss

# print(get_os(url))

def last_seen(url):
    try:
        ls = snapshots[-1]
        return ls
    except:
        return datetime.now()

# print(last_seen(url))

def days_since_last_seen(url):
    dsls = (datetime.today()-last_seen(url)).days
    return dsls

# print(days_since_last_seen(url))

def days_since_first_seen(url):
    dsfs = (datetime.today()-first_seen(url)).days
    return dsfs

# print(days_since_first_seen(url))

def average_update_frequency(url):
    snapshots = get_site_snapshots(url)
    diffs = [(t-s).days for s, t in zip(snapshots, snapshots[1:])]
    l = len(diffs)
    if l > 0:
        return sum(diffs)/l
    else:
        return 0

# print(average_update_frequency(url))

def number_of_updates(url):
    snapshots = get_site_snapshots(url)
    return len(snapshots)

# print(number_of_updates(url))

def ttl_from_registration(url):
    earliest_date_seen = first_seen(url)
    try:
        ttl_from_reg = (earliest_date_seen - url_creation_date(url)[1]).days
    except:
        ttl_from_reg = None
    return ttl_from_reg

# print(ttl_from_registration(url))

