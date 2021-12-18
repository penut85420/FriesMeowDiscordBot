import os
import sys
import json
import datetime as dt

from loguru import logger


def set_logger():
    log_format = (
        '{time:YYYY-MM-DD HH:mm:ss.SSSSSS} | '
        '<lvl>{level: ^9}</lvl> | '
        '{message}'
    )
    logger.add(sys.stderr, level='INFO', format=log_format)
    logger.add(
        f'./logs/system.log',
        rotation='1 day',
        retention='7 days',
        level='INFO',
        encoding='UTF-8',
        compression='gz',
        format=log_format
    )


set_logger()
logger.info('Logging initialize done')

TMP_PATH = './config/tmp'
CONFIG_PATH = './config/config.json'


def load_config():
    return load_json(CONFIG_PATH)


def load_json(file_path):
    return json.load(open(file_path, 'r', encoding='UTF-8'))


def walk_dir(dir_path):
    for dirPath, _, fileList in os.walk(dir_path):
        for fileName in fileList:
            fullPath = os.path.join(dirPath, fileName)
            yield fullPath, fileName


def to_int(args):
    try:
        return int(args[0]), 1
    except:
        return 1, 0


def exchange_name(msg):
    exchange_list = [
        ('我', '!@#$1$#@!'),
        ('my', '!@#$2$#@!'),
        ('My', '!@#$3$#@!'),
        ('MY', '!@#$4$#@!'),
        ('你', '我'),
        ('妳', '我'),
        ('您', '我'),
        ('!@#$1$#@!', '你'),
        ('!@#$2$#@!', 'your'),
        ('!@#$3$#@!', 'Your'),
        ('!@#$4$#@!', 'YOUR'),
    ]

    for sub, repl in exchange_list:
        msg = msg.replace(sub, repl)
    return msg


class BotUtils:
    def __init__(self):
        self.config = load_config()
        self.restart_channel = self.config['restart_channel']
        self.start_time = dt.datetime.now()
        self.config['is_debug'] = self.config['is_debug'] == "True"
        self.dev_id_dict = dict()
        for dev_id in [int(line) for line in self.config['dev_id']]:
            self.dev_id_dict[dev_id] = True

    def is_dev(self, ctx):
        user_id = ctx.author.id
        return self.dev_id_dict.get(user_id, False)

    def get_token(self):
        token_key = 'token_test' if self.config['is_debug'] else 'token'
        return self.config[token_key]

    def get_ignore_channels(self):
        return self.config['ignore_channels']

    def get_build_time(self):
        return self.start_time.strftime('%Y-%m-%d %H:%M:%S')

    async def not_dev_msg(self, ctx):
        await ctx.send('%s 你不是開發人員，不能用這個指令 (((ﾟдﾟ)))' % ctx.author.name)
