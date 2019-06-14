import json
import bot_util as btl
import random

class FortuneMeow:
    def __init__(self):
        self.fortune = btl.load_json('./data/fortune.json')
    
    def _parse_result(self, result):
        rtn = list()
        for k in result:
            rtn.append('%s：%s' % (k, result[k]))
        return '\n'.join(rtn)

    def get_fortune(self):
        r = random.randint(0, 99)
        f = self.fortune[r]
        msg = '[%s] %s\n\n%s\n\n%s' % (f['type'], f['poem'], f['explain'], self._parse_result(f['result']))
        return msg

if __name__ == '__main__':
    fm = FortuneMeow()
    print(fm.get_fortune())