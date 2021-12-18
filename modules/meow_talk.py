import random


class MeowTalk:
    def __init__(self):
        self.end = [
            '!',
            '～',
            '!!',
            ' >ω<',
            ' Φ౪Φ',
            ' ฅ●ω●ฅ',
            ' (=´ᴥ`)',
            ' ( Φ ω Φ )',
            ' (=^-ω-^=)',
            ' ヾ(*ΦωΦ)ツ',
            ' ヽ(=^･ω･^=)丿',
        ]

    def get_sent(self):
        n = self.get_norm_rand(5)
        sent = []
        for i in range(n):
            if sent:
                sent.append('，')
            sent.append(self.get_meow())
        sent.append(self.get_rand_end())
        return ''.join(sent)

    def get_rand_end(self):
        return random.choice(self.end)

    def get_meow(self):
        t = self.get_norm_rand(5) + 1
        return t * '喵'

    def get_norm_rand(self, n):
        p = self.gen_prob(n)
        return random.choices(range(n), weights=p)[0]

    def gen_prob(self, n):
        n1 = n // 2
        n2 = n - n1

        p1, p2 = map(list, map(range, (n1, n2)))
        p2 = [p for p in reversed(p2)]

        p = p1 + p2
        p = [p + 1 for p in p]

        return p


if __name__ == '__main__':
    mt = MeowTalk()
    for i in range(1, 10):
        print(mt.get_sent())
