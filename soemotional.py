from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle as pk
import random

class SoEmotional:
    def __init__(self):
        self.init_vectorizer()
        with open('./data/data.pkl', 'rb') as pkl:
            self.data = pk.load(pkl)
        self.keys = list(self.data.keys())
    
    def init_vectorizer(self):
        vec = TfidfVectorizer(analyzer='char')
        with open('./data/raw.pkl', 'rb') as pkl:
            data = pk.load(pkl)
        self.vec = vec.fit(data)

    def calc_cos(self, s1, s2):
        ss = [s1, s2]
        s1, s2 = self.vec.transform(ss).toarray()
        s1 = s1.reshape(1, -1)
        s2 = s2.reshape(1, -1)
        return cosine_similarity(s1, s2)
    
    def get_response(self, msg):
        msg = ' '.join(msg.replace(' ', ''))
        max_result = (0, None)
        rndlen = random.randint(4000, 7000)
        gap = random.randint(70, 85) / 100
        random.shuffle(self.keys)
        for d in self.keys[:rndlen]:
            r = self.calc_cos(' '.join(d), msg)
            if r > max_result[0]:
                max_result = (r, self.data[d])
            if max_result[0] > gap:
                break
        return max_result[1]

    def get_responses(self, msg):
        msg = ' '.join(msg.replace(' ', ''))
        max_result = (0, None)
        rndlen = random.randint(4000, 7000)
        gap = random.randint(70, 85) / 100
        random.shuffle(self.keys)
        for d in self.keys[:rndlen]:
            r = self.calc_cos(' '.join(d), msg)
            if r > max_result[0]:
                max_result = (r, self.data[d])
            if max_result[0] > gap:
                break
        res = max_result[1]
        ress = [res]
        for _ in range(random.randint(2, 5)):
            nextres = self.data.get(res)
            if not nextres:
                break
            ress.append(self.data[res])
        return ress

if __name__ == '__main__':
    se = SoEmotional()

    ss = [
        '我心情很好',
        '我心情好啊',
        '心情真是不錯',
        '我心情不好',
        '我想睡覺',
        '我好難過',
        '為什麼她不愛我',
        '我該告白嗎'
    ]
    
    for s in ss:
        print('Search for %s' % s)
        res = se.get_responses(s)
        print('Response ' + str(res))
