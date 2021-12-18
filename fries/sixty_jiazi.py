import json
import random


class SixtyJiazi:
    def __init__(self):
        with open('./data/sixty_jiazi.json', 'r', encoding='UTF-8') as fin:
            self.poems = json.load(fin)

    def pick(self):
        r = random.randint(0, 59)
        def concat(x): return '\n'.join(x)

        poem = self.poems[r]
        title = poem['title']
        gua = concat(poem['gua'])
        poemt = concat(poem['poem'])
        item = concat(poem['item'])
        story = concat(poem['story'])
        detail = f'http://www.ma-tsu.com.tw/lot_go.asp?anum={r+1}'

        result = f'**{title}**\n\n{gua}\n\n{poemt}\n\n{item}\n\n參考故事：\n{story}\n\n詳解網站：\n<{detail}>'
        return result


if __name__ == "__main__":
    sj = SixtyJiazi()
    print(sj.pick())
