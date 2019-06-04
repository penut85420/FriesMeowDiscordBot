import json
import logging
import os
import subprocess as sp
import sys
import time

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)-20s %(message)s', '%Y-%m-%d %H:%M:%S')
console.setFormatter(formatter)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
    handlers=[console]
)

log = logging.getLogger('fries.meow.mainloop')
log.info('Begin main loop')

run = json.load(open('./config/config.json', 'r', encoding='UTF-8'))['run']
while True:
    try:
        sp.call([run, 'main.py'])
        if os.path.exists('./config/tmp'):
            code = int(open('./config/tmp', 'r', encoding='UTF-8').read())
            if code:
                log.info('Bot is shutdown')
                break
        log.info('Bot restart...')
        # time.sleep(1)
    except KeyboardInterrupt:
        exit(0)
