#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys

def procedure(keyword):
    url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%s&page=1&sort=new/dc' % (keyword)

    r = requests.get(url);

if __name__ == '__main__':
    procedure(sys.argv[1])
