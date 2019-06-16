import json
import os
import time
import xml.etree.cElementTree as xml
from datetime import datetime as dt

import requests


class RssPost:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def __str__(self):
        return '%s\n%s' % (self.title.strip(), self.link.strip())


class RssSubscriber:
    def __init__(self, url, pt, tag=dict(), encoding='UTF-8'):
        self.url = url
        self.time_pt = pt
        self.init_tags(tag)
        self.encoding = encoding
        self.update()

    def init_tags(self, tag):
        self.tag = {
            'channel': 'channel',
            'last_build_date': 'lastBuildDate',
            'item': 'item',
            'title': 'title',
            'link': 'link',
        }

        for k in tag:
            self.tag[k] = tag[k]

    def update(self):
        self.request = requests.get(self.url)
        self.xml = xml.XML(self.request.content.decode(self.encoding))
        channel = self.xml.find(self.tag['channel'])
        self.last_build_date = channel.find(self.tag['last_build_date']).text
        self.last_build_date = dt.strptime(self.last_build_date, self.time_pt)
        self.rss = list()
        self.map = dict()
        for item in channel.findall(self.tag['item']):
            title = item.find(self.tag['title']).text
            link = item.find(self.tag['link']).text
            itemd = {
                'title': title,
                'link': link,
            }
            post = RssPost(**itemd)
            self.rss.append(post)
            self.map[title] = post

    def __eq__(self, another):
        rss1 = self.rss
        rss2 = another.rss
        if len(rss1) != len(rss2):
            return False

        for r1, r2 in tuple(zip(rss1, rss2)):
            if r1.title != r2.title:
                return False
        return True

    def __sub__(self, another):
        if self == another:
            return list()

        rtn = list()
        for m in self.map:
            if not another.map.get(m, None):
                rtn.append(self.map[m])

        return rtn


class GnnRss(RssSubscriber):
    """巴哈姆特 GNN 新聞網"""
    def __init__(self):
        self.url = 'https://gnn.gamer.com.tw/rss.xml'
        self.time_pt = '%a, %d %b %Y %H:%M:%S CST'
        self.encoding = 'CP950'
        super().__init__(self.url, self.time_pt, encoding=self.encoding)


class FreeGroupRss(RssSubscriber):
    """免費資源網路社群"""
    def __init__(self):
        self.url = 'http://feeds.feedburner.com/freegroup?format=xml'
        self.time_pt = '%a, %d %b %Y %H:%M:%S +0000'
        super().__init__(self.url, self.time_pt)


class UdnRss(RssSubscriber):
    """聯合新聞網"""
    def __init__(self, url):
        self.url = url
        self.time_pt = '%a, %d %b %Y %H:%M:%S +0800'
        tag = {'last_build_date': 'pubDate'}
        super().__init__(self.url, self.time_pt, tag)


class UdnGameRss(UdnRss):
    """聯合新聞網瘋電競賽事快訊"""
    def __init__(self):
        self.url = 'https://game.udn.com/rss/news/2003/10444/10445?ch=game'
        super().__init__(self.url)


class UdnAnimeRss(UdnRss):
    """聯合新聞網動漫影視新聞"""
    def __init__(self):
        self.url = 'https://game.udn.com/rss/news/2003/10452/12982?ch=game'
        super().__init__(self.url)


class ToyPeopleRss(RssSubscriber):
    """玩具人"""
    def __init__(self):
        self.url = 'https://feeds.feedburner.com/toy-people?format=xml'
        self.time_pt = '%a, %d %b %Y %H:%M:%S +0800'
        super().__init__(self.url, self.time_pt)


class TestRss(RssSubscriber):
    """RSS Test"""
    def __init__(self):
        self.url = 'http://127.0.0.1:5000/'
        self.time_pt = '%a, %d %b %Y %H:%M:%S CST'
        super().__init__(self.url, self.time_pt)


class RssMan:
    CHANNEL_PATH = './data/channel.json'

    def __init__(self):
        self.cls = [
            FreeGroupRss,
            GnnRss,
            ToyPeopleRss,
            UdnAnimeRss,
            UdnGameRss,
        ]
        self.init_rss()
        self.init_channel()

    def init_rss(self):
        self.rss_group = dict()
        for c in self.cls:
            self.rss_group[c.__doc__] = c()

    def init_channel(self):
        if not os.path.exists(RssMan.CHANNEL_PATH):
            with open(RssMan.CHANNEL_PATH, 'w') as fout:
                json.dump(list(), fout)

        with open(RssMan.CHANNEL_PATH, 'r', encoding='UTF-8') as fin:
            self.channel = json.load(fin)

    def update(self):
        rtn = dict()
        for clsn in self.cls:
            name = clsn.__doc__
            c1 = self.rss_group[name]
            c2 = clsn()
            if c2 != c1:
                arr = rtn.get(name, list())
                for post in c2 - c1:
                    arr.append(post)
                rtn[name] = arr
                self.rss_group[name] = c2
        return rtn

    def register(self, channel):
        if channel not in self.channel:
            self.channel.append(channel)
        with open(RssMan.CHANNEL_PATH, 'w', encoding='UTF-8') as fout:
            json.dump(self.channel, fout)


if __name__ == '__main__':
    RssMan()
