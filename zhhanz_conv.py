import pickle as pk

class ZhhanzMan:
    def __init__(self):
        with open('./zhhanz.pkl', 'rb') as pkl:
            self.dict = pk.load(pkl)
    
    def max_match(self, sent, d):
        for n in d['length']:
            seg = sent[:n]
            if d['dict'][n].get(seg, None):
                return d['dict'][n].get(seg)
            n -= 1
        return sent[0]
    
    def trans_s2t(self, sent):
        return self.trans(sent, self.dict['s2t'])
    
    def trans_t2s(self, sent):
        return self.trans(sent, self.dict['t2s'])
    
    def trans(self, sent, d):
        rtn = list()
        idx = 0
        while idx < len(sent):
            r = self.max_match(sent[idx:], d)
            idx += len(r)
            rtn.append(r)
        return ''.join(rtn)

if __name__ == '__main__':
    s2t = [
        '硬盘上无法修复的坏轨，',
        '可能导致硬盘使用上产生异常的现象，',
        '例如：存取缓慢、当机、档案毁损等症状发生。',
        '最近上市的固态硬盘也会使用广泛使用于 DRAM 内存的 ECC 技术来保护快闪存储器资料。',
        '網誌（英语：Blog）是一種由个人管理、張貼新的文章、圖片或影片的網站或線上日記，',
        '用來紀錄、抒發情感或分享資訊。',
        '網誌上的文章通常根據張貼時間，',
        '以倒序方式由新到舊排列。',
        '许多博客作者專注评论特定的课题或新闻，',
        '其他則作为個人日记。',
        '一个典型的博客结合了文字、图像、其他博客或网站的超連結、及其它與主题相关的媒体。',
        '能够让读者以互动的方式留下意见，',
        '是许多博客的重要要素。',
        '大部分的博客內容以文字为主，',
        '也有一些博客專注艺术、攝影、视频、音乐、播客等各種主題。',
        '網誌是社会媒体网络的一部分。',
        '皇后在后面吃面',
        '艦隊Collection 是日本网络游戏', 
        '是消歧义页面', 
        '陈公乾生'
    ]
    t2s = list()
    zm = ZhhanzMan()
    with open('s2t', 'w', encoding='UTF-8') as fout:
        for ss in s2t:
            t2s.append(zm.trans_s2t(ss))
            print(t2s[-1], file=fout)
    
    with open('t2s', 'w', encoding='UTF-8') as fout:
        for ss in t2s:
            print(zm.trans_t2s(ss), file=fout)
