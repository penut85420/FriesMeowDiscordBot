import urllib
import requests
import json

class WikiMan:
    def __init__(self):
        self.wiki_url = 'https://zh.wikipedia.org/zh-tw/'
        self.query_page = 'https://zh.wikipedia.org/w/api.php?action=query&titles=%s&prop=description|extracts&format=json&exintro=&explaintext=&variant=zh-tw&redirects'

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
            title = page['title']
            desc = page.get('description', None)
            if desc == '维基百科消歧义页':
                desc = '維基百科消歧義頁面'
            contents = page.get('extract', None)
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