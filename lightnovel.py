#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedgen.feed
import lxml.html
import re
import requests

def procedure():
    url = 'https://24h.pchome.com.tw/?m=store&f=book_show&RG_NO=DJAZ&pageType=0'

    r = requests.get(url);
    r.encoding = 'big5';

    html = lxml.html.fromstring(r.text)
    title = html.cssselect('title')[0].text_content()

    book_date_re = re.compile('出版日：\s*(\S+)', re.M)
    book_publisher_re = re.compile('出版社：\s*(\S+)', re.M)

    feed = feedgen.feed.FeedGenerator()
    feed.id(url)
    feed.link(href=url, rel='self')
    feed.title(title)

    for table in html.cssselect('#StoreBodyContainer table[width="360"]'):
        try:
            a = table.cssselect('.text13')[0]
            book_name = a.text_content()
            book_url = a.get('href')

            table_txt = table.text_content()

            book_date = book_date_re.search(table_txt)[0]
            book_publisher = book_publisher_re.search(table_txt)[0]

            k = '%s - %s - %s' % (book_name, book_publisher, book_date)

            entry = feed.add_entry()
            entry.id(book_url)
            entry.title(k)
            entry.link(href=book_url)

        except IndexError:
            pass

    print(str(feed.atom_str(), 'utf-8'))

if __name__ == '__main__':
    procedure()
