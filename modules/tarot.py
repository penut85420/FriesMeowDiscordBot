import json
import logging
import random
import re

KEY_REVERSED = ['positive', 'reversed']
STR_REVERSED = ['正位', '逆位']
STR_COLUMN = {
    "behavior": "行為暗示",
    "marriage": "婚姻",
    "meaning": "解釋",
    "related": "相關詞",
    "sexuality": "兩性關係",
}

DETAIL_ORDER = ['related', 'behavior', 'meaning', 'sexuality', 'marriage']
SIMPLE_ORDER = ['related', 'meaning']


class TarotMeow:
    def __init__(self):
        with open('./data/tarot_cht.json', 'r', encoding='UTF-8') as fin:
            self.tarot = json.load(fin)
        self.logger = logging.getLogger('fries.meow.tarot')

    def get_tarot(self):
        i, r = self._get_tarot_info()
        return self._get_tarot_msg_path(i, r)

    def _get_tarot_msg_path(self, i, r):
        msg = self._get_tarot_msg(i, r)
        path = self._get_tarot_path(i, r)
        return msg, path

    def get_many_tarot(self, n):
        if n > 156:
            n = 156
        if n < 1:
            n = 1
        arr = list(range(78*2))
        random.shuffle(arr)
        for i in range(n):
            yield self._get_tarot_msg_path(arr[i] // 2, arr[i] % 2)

    def _get_tarot_info(self):
        ri = random.randint(0, 77)
        rr = random.randint(0, 1)
        return ri, rr

    def _get_tarot_path(self, i, r):
        return './tarot/%02d%s.jpg' % (i, 'r' if r else '')

    def _get_tarot_msg(self, i, r):
        tarot = self.tarot['%02d' % i]
        card = tarot[KEY_REVERSED[r]]
        msg = '**%s%s**\n\n' % (STR_REVERSED[r], tarot['name'])
        msg += self._parse_result_detail(card)
        self.logger.info('Response %s%s' % (STR_REVERSED[r], tarot['name']))
        return msg

    def _parse_result_detail(self, r):
        rtn = list()
        for k in DETAIL_ORDER:
            rtn.append('**%s**\n%s' % (STR_COLUMN[k], r[k]))
        return '\n\n'.join(rtn)

    def _init_query_dict(self):
        self.query = dict()
        card_name = list()
        for idx in self.tarot:
            name = self.tarot[idx]['name']
            self.query[name] = idx
            card_name.append(name)
        self.query_pattern = re.compile('(%s)' % '|'.join(card_name))

    def is_reversed(self, term):
        if '反' in term:
            return 1
        if '逆' in term:
            return 1
        return 0

    def query_card(self, query):
        query_card = self.query_pattern.findall(query)[0]
        query_dir = self.is_reversed(term)


if __name__ == '__main__':
    tm = TarotMeow()
    print(tm.get_tarot()[0])
