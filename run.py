import time
import subprocess as sp
import sys
import json
import os

run = json.load(open('./config/config.json', 'r', encoding='UTF-8'))['run']

while True:
    try:
        sp.call([run, 'main.py'])
        if os.path.exists('./config/tmp'):
            code = int(open('./config/tmp', 'r', encoding='UTF-8').read())
            if code:
                print('Bot is shutdown')
                break
        print('Bot restart...')
        # time.sleep(1)
    except KeyboardInterrupt:
        exit(0)
