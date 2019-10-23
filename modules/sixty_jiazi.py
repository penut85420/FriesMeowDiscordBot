import json
import random

class SixtyJiazi:
    def __init__(self):
        with open('./data/sixty_jiazi.json', 'r', encoding='UTF-8') as fin:
            self.poems = json.load(fin)
    
    def pick(self):
        r = random.randint(0, 59)
        concat = lambda x: '\n'.join(x)
        
        poem = self.poems[r]
        title = poem['title']
        gua = concat(poem['gua'])
        poemt = concat(poem['poem'])
        item = concat(poem['item'])
        story = concat(poem['story'])

        result = f'**{title}**\n\n{gua}\n\n{poemt}\n\n{item}\n\n參考故事：\n{story}'
        return result

if __name__ == "__main__":
    sj = SixtyJiazi()
    print(sj.pick())