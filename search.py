#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedgen.feed
import json
import requests
import sys

def procedure(keyword):
    url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%s&page=1&sort=new/dc' % (keyword)

    r = requests.get(url);

    title = 'PChome 搜尋 - %s' % (keyword)

    feed = feedgen.feed.FeedGenerator()
    feed.author({'name': 'PChome Search Feed Generator'})
    feed.id(url)
    feed.link(href=url, rel='alternate')
    feed.title(title)

    body = json.loads(r.text)

    print(str(feed.atom_str(), 'utf-8'))

if __name__ == '__main__':
    procedure(sys.argv[1])
