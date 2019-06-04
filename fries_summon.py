import os
import bot_util as btl
import random

class FriesSummoner:
    def __init__(self):
        self.origin_list = list()
        for fullPath, _ in btl.walk_dir('./fries_pictures'):
            self.origin_list.append(fullPath)
        self._shuffle()
        
    def _shuffle(self):
        self.shuffle_list = self.origin_list.copy()
        random.shuffle(self.shuffle_list)
    
    def _pop(self):
        rtn = self.shuffle_list[0]
        self.shuffle_list.remove(rtn)

        return rtn
    
    def _is_empty(self):
        return len(self.shuffle_list) == 0
    
    def _get_picture(self):
        if self._is_empty():
            self._shuffle()
        return self._pop()
    
    def get_pictures(self, n):
        for _ in range(n):
            yield self._get_picture()

if __name__ == '__main__':
    fs = FriesSummoner()
    for y in fs.get_pictures(16):
        print(y)