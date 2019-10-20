import sys
sys.path.append('..')
import json
import urllib
import requests
from zhhanz_conv import ZhhanzMan

class WikiMan:
    def __init__(self):
        with open('./data/wiki.json', 'r', encoding='UTF-8') as fin:
            config = json.load(fin)
        self.wiki_url = config['wiki']
        self.query_page = config['query']
        self.zhman = ZhhanzMan()

    def query(self, term):
        term = self._encode(term)
        query_url = self.query_page % term
        result = requests.get(query_url)
        return json.loads(result.text)

    def get_summary(self, *term):
        query_results = self.query('|'.join(term))
        query_pages = list(query_results['query']['pages'].values())
        rtn_results = dict()
        for page in query_pages:
            title = self.zhman.trans_s2t(page['title'])
            desc = page.get('description', None)
            if desc:
                desc = self.zhman.trans_s2t(desc)
            contents = page.get('extract', None)
            if contents:
                contents = self.zhman.trans_s2t(contents)
            rtn_results[title] = dict()
            rtn_results[title]['desc'] = desc
            rtn_results[title]['contents'] = contents
        return rtn_results

    def get_response(self, *terms):
        results = self.get_summary(*terms)
        responses = list()
        for title in results:
            msg = ['**%s**' % title]
            if results[title]['desc']:
                msg.append(' 是%s' % results[title]['desc'])
            if results[title]['contents']:
                msg.append('\n\n%s' % results[title]['contents'])
                msg.append('\n\n%s%s' % (self.wiki_url, title))
            else:
                msg.append('\n\n沒有找到關於 %s 的維基頁面。' % title)
            responses.append(''.join(msg))
        return responses

    def _encode(self, term):
        return urllib.parse.quote(term)


if __name__ == '__main__':
    terms = ['孫中山', '魔法少女小圓', 'AKB48']
    wm = WikiMan()
    for r in wm.get_response(*terms):
        print(r)
