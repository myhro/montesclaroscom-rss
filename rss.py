# -*- coding: utf-8 -*-

from datetime import datetime
import re
import urllib2
import bs4
import PyRSS2Gen
import pytz


class MontesClarosComRSS:
    def __init__(self):
        self.date_pattern_hour_only = re.compile('.* (\d+\/\d+\/\d+ - \d+h)')
        self.date_pattern_hour_with_minute = re.compile('.* (\d+\/\d+\/\d+ - \d+h\d+)')
        self.feed = None
        self.soup = None

    def generate_feed(self):
        if not self.soup:
            self.soup = self.load_content()
            self.titles = self.soup.find_all('span')
            self.total = len(self.titles)
        rss_items = []
        for i in xrange(0, self.total, 3):
            span_date, span_title, span_content = self.titles[i:i+3]
            date_format = '%d/%m/%y - %Hh%M'
            matched_date = re.match(self.date_pattern_hour_with_minute, span_date.text)
            if not matched_date:
                date_format = '%d/%m/%y - %Hh'
                matched_date = re.match(self.date_pattern_hour_only, span_date.text)
            converted_date = datetime.strptime(matched_date.group(1), date_format)
            item_date = self.naive_to_utc(converted_date)
            item_title = span_title.text.strip()
            item_link = u'http://montesclaros.com' + span_title.a['href']
            item_content = span_content.text.strip()
            new_item = PyRSS2Gen.RSSItem(
                title = item_title,
                link = item_link,
                description = item_content,
                pubDate = item_date
            )
            rss_items.append(new_item)
        build_date = self.naive_to_utc(datetime.now())
        self.feed = PyRSS2Gen.RSS2(
            title = u'montesclaros.com',
            link = 'http://montesclaros.com/',
            description = u'Um olhar de Montes Claros sobre o que é notícia em toda parte',
            lastBuildDate = build_date,
            items = rss_items,
        )

    def load_content(self):
        return bs4.BeautifulSoup(urllib2.urlopen('http://montesclaros.com/').read())

    def naive_to_utc(self, naive_date):
        brtz = pytz.timezone('America/Sao_Paulo')
        aware_date_local = brtz.localize(naive_date)
        aware_date_utc = aware_date_local.astimezone(pytz.utc)
        return aware_date_utc

    def save_feed(self):
        if not self.feed:
            self.generate_feed()
        self.feed.write_xml(open('feed.xml', 'w'))


if __name__ == '__main__':
    rss = MontesClarosComRSS()
    rss.save_feed()
