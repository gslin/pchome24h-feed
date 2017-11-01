#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedgen.feed
import html
import json
import requests
import sys
import urllib

def magic(keyword):
    url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%s&page=1&sort=new/dc' % (urllib.parse.quote_plus(keyword))

    r = requests.get(url);

    title = 'PChome 搜尋 - %s' % (keyword)

    feed = feedgen.feed.FeedGenerator()
    feed.author({'name': 'PChome Search Feed Generator'})
    feed.id(url)
    feed.link(href=url, rel='alternate')
    feed.title(title)

    body = json.loads(r.text)

    for prod in body['prods']:
        try:
            # Product name & description
            prod_name = prod['name']
            prod_desc = prod['describe']

            # URL
            if prod['cateId'][0] == 'D':
                prod_url = 'https://24h.pchome.com.tw/prod/' + prod['Id']
            else:
                prod_url = 'https://mall.pchome.com.tw/prod/' + prod['Id']
            img_url = 'https://a.ecimg.tw%s' % (prod['picB'])

            body = '%s<br/><img alt="" src="%s"/>' % (html.escape(prod_desc), html.escape(img_url))

            entry = feed.add_entry()
            entry.content(body, type='xhtml')
            entry.id(prod_url)
            entry.link(href=prod_url)
            entry.title(prod_name)

        except:
            pass

    print(str(feed.atom_str(), 'utf-8'))

if __name__ == '__main__':
    magic(sys.argv[1])
