#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedgen.feed
import lxml.html
import re
import selenium
import selenium.webdriver.chrome.options

def magic():
    url = 'https://24h.pchome.com.tw/books/store/?q=/R/DJAZ/new'

    chrome_options = selenium.webdriver.chrome.options.Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.binary_location = '/usr/bin/chromium-browser'

    b = selenium.webdriver.Chrome(chrome_options=chrome_options)
    b.get(url)
    html = b.find_element_by_tag_name('html').get_attribute('innerHTML')
    b.close()

    html = lxml.html.fromstring(html)
    title = html.cssselect('title')[0].text_content()

    feed = feedgen.feed.FeedGenerator()
    feed.author({'name': 'PChome 24h Feed Generator'})
    feed.id(url)
    feed.link(href=url, rel='alternate')
    feed.title(title)

    for item in html.cssselect('#ProdListContainer'):
        try:
            a = item.cssselect('.prod_name a')[0]
            book_name = a.text_content()

            book_url = a.get('href')
            if re.match('//', book_url):
                book_url = 'https:' + book_url

            item_txt = item.text_content()

            book_date = re.search('出版日：\s*(\S+)', item_txt, re.M)[0]
            book_publisher = re.search('出版社：\s*(\S+)', item_txt, re.M)[0]

            k = '%s - %s - %s' % (book_name, book_publisher, book_date)

            entry = feed.add_entry()
            entry.id(book_url)
            entry.title(k)
            entry.link(href=book_url)

        except IndexError:
            pass

    print(str(feed.atom_str(), 'utf-8'))

if __name__ == '__main__':
    magic()
