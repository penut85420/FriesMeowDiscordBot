import json
import os
import random
import unittest
from os.path import join

TEMPLATE_DIR_PATH = './template'


class ResponseTemplate:
    def __init__(self):
        self.load()

    def get_response(self, key, *args):
        tmp = self.template.get(key, None)
        if not tmp:
            return None
        if type(tmp) == list:
            r = random.randint(0, len(tmp)-1)
            return tmp[r] % args
        return self.template[key] % args

    def load(self):
        self.template = dict()
        for dirPath, _, fileList in os.walk(TEMPLATE_DIR_PATH):
            for fileName in fileList:
                fullPath = join(dirPath, fileName)
                if fileName.endswith('.json'):
                    self.load_json(fullPath, fileName)
                else:
                    self.load_data(fullPath, fileName)

    def load_data(self, full_path, file_name):
        with open(full_path, 'r', encoding='UTF-8') as fin:
            self.template[file_name] = fin.read()

    def load_json(self, full_path, file_name):
        contents = json.load(open(full_path, 'r', encoding='UTF-8'))
        self.template[file_name[:-5]] = contents


if __name__ == '__main__':
    rt = ResponseTemplate()
    print(rt.get_response('hello', '大歐派蘿莉'))
    # print(rt.get_response('twsc', 'Hello'))
