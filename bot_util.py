import os
import json
import pickle as pk

TMP_PATH = './config/tmp'
CONFIG_PATH = './config/config.json'

def load_config():
    return load_json(CONFIG_PATH)

def mk_mention(ctx):
    return '<@%s>' % ctx.author.id

def load_json(file_path):
    return json.load(open(file_path, 'r', encoding='UTF-8'))

def load_pkl(file_path):
    return pk.load(open(file_path, 'rb'))

def walk_dir(dir_path):
    for dirPath, _, fileList in os.walk(dir_path):
        for fileName in fileList:
            fullPath = os.path.join(dirPath, fileName)
            yield fullPath, fileName

def cast_int(args):
    try:
        return int(args[0]), 1
    except:
        return 1, 0

def write_file(file_path, contents):
    with open(file_path, 'w', encoding='UTF-8') as fout:
        fout.write(contents)

def restart_bot():
    write_file(TMP_PATH, '0')

def shutdown_bot():
    write_file(TMP_PATH, '1')

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
        ('!@#$2$#@!', '你'),
        ('!@#$3$#@!', '你'),
        ('!@#$4$#@!', '你'),
    ]
    
    for sub, repl in exchange_list:
        msg = msg.replace(sub, repl)
    return msg

class BotUtils:
    def __init__(self):
        self.config = load_config()
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

    async def not_dev_msg(self, ctx):
        await ctx.send('%s 你不是開發人員，不能用這個指令 (((ﾟдﾟ)))' % ctx.author.name)