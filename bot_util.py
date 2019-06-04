import os
import json
import pickle as pk

def get_token():
    token_path = 'token_test' if os.path.exists('./debug') else 'token'
    return open(token_path, 'r').read()

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
        self.dev_id_dict = dict()
        for dev_id in [int(line) for line in open('./dev_id', 'r')]:
            self.dev_id_dict[dev_id] = True
    
    def is_dev(self, ctx):
        user_id = ctx.author.id
        return self.dev_id_dict.get(user_id, False)
    
    async def not_dev_msg(self, ctx):
        await ctx.send('%s 你不是開發人員，不能用這個指令 (((ﾟдﾟ)))' % ctx.author.name)