import json
import random


class FortuneMeow:
    def __init__(self):
        with open('./data/fortune.json', 'r', encoding='UTF-8') as fin:
            self.fortune = json.load(fin)

    def parse_result(self, result):
        rtn = list()
        for k in result:
            rtn.append('%s：%s' % (k, result[k]))
        return '\n'.join(rtn)

    def get_fortune(self):
        r = random.randint(0, 99)
        f = self.fortune[r]
        msg = '[%s] %s\n\n%s\n\n%s' % (
            f['type'], f['poem'], f['explain'], self.parse_result(f['result']))
        return msg


if __name__ == '__main__':
    fm = FortuneMeow()
    print(fm.get_fortune())
