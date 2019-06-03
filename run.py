import time
import subprocess as sp
import sys

while True:
    try:
        sp.call(['py', 'main.py'])
        code = int(open('tmp', 'r', encoding='UTF-8').read())
        if code:
            print('Bot is shutdown')
            break
        print('Bot restart after 1 seconds')
        time.sleep(1)
    except KeyboardInterrupt:
        exit(0)
