# -*- coding: utf-8 -*-

import unittest
import bs4
import mock
from rss import MontesClarosComRSS


@mock.patch('rss.MontesClarosComRSS.load_content')
class MontesClarosComRSSTestCase(unittest.TestCase):
    def test_save(self, mocked_load_content):
        mocked_load_content.return_value = bs4.BeautifulSoup(open('index.html').read())
        rss = MontesClarosComRSS()
        rss.save_feed()


if __name__ == '__main__':
    unittest.main()
