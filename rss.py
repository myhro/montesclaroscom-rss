# -*- coding: utf-8 -*-

from datetime import datetime
import re
import urllib2
import bs4
import PyRSS2Gen

soup = bs4.BeautifulSoup(urllib2.urlopen('http://montesclaros.com/').read())
titles = soup.find_all('span')
total = len(titles)

date_pattern_hour_only = re.compile('.* (\d+\/\d+\/\d+ - \d+h)')
date_pattern_minute = re.compile('.* (\d+\/\d+\/\d+ - \d+h\d+)')

rss_items = []

for i in xrange(0, total, 3):
    date_format = '%d/%m/%y - %Hh%M'
    span_date = re.match(date_pattern_minute, titles[i].text)
    if not span_date:
        date_format = '%d/%m/%y - %Hh'
        span_date = re.match(date_pattern_hour_only, titles[i].text)
    item_date = datetime.strptime(span_date.group(1), date_format)
    item_title = titles[i+1].text.strip()
    item_link = u'http://montesclaros.com' + titles[i+1].a['href']
    item_content = titles[i+2].text.strip()
    new_item = PyRSS2Gen.RSSItem(
        title = item_title,
        link = item_link,
        description = item_content,
        pubDate = item_date
    )
    rss_items.append(new_item)

rss = PyRSS2Gen.RSS2(
    title = u'montesclaros.com',
    link = 'http://montesclaros.com/',
    description = u'Um olhar de Montes Claros sobre o que é notícia em toda parte',
    lastBuildDate = datetime.now(),
    items = rss_items,
)

rss.write_xml(open('feed.xml', 'w'))
