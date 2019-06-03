import json

def mk_mention(ctx):
    return '<@%s>' % ctx.author.id

def load_json(file_path):
    return json.load(open(file_path, 'r', encoding='UTF-8'))

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