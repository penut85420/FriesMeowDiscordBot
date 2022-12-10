import json
import random
import re
from loguru import logger


KEY_REVERSED = ["positive", "reversed"]
STR_REVERSED = ["正位", "逆位"]
STR_COLUMN = {
    "behavior": "行為暗示",
    "marriage": "婚姻",
    "meaning": "解釋",
    "related": "相關詞",
    "sexuality": "兩性關係",
}

DETAIL_ORDER = ["related", "behavior", "meaning", "sexuality", "marriage"]
SIMPLE_ORDER = ["related", "meaning"]


class TarotMeow:
    def __init__(self):
        with open("./data/tarot_cht.json", "r", encoding="UTF-8") as fin:
            self.tarot = json.load(fin)
        self._init_query_dict()
        self.prompt = "你現在是一個專業的塔羅牌占卜師，而且你的身份是貓咪，所以你總是使用「喵喵」做為句末助詞或者口頭禪。我會輸入一個問題，以及一張塔羅牌，你必須根據這張塔羅牌所代表的涵義，針對提出的問題給出詳細的解釋。塔羅牌分成正位與逆位，有時逆位並不代表該牌完全相反的意義。在解釋問題時，請盡量往正面、積極的方向做解釋。在這個過程中，你不能透露你是 AI，也不能透露你是語言模型，也不要向我要求更多訊息。現在占卜開始。"

    def get_gpt_tarot(self, problem):
        i, r = self._get_tarot_info()
        img_path = self._get_tarot_path(i, r)
        tarot = self.tarot["%02d" % i]
        card = tarot[KEY_REVERSED[r]]
        related: str = card["related"]
        related = related.strip("。")
        card_name = STR_REVERSED[r] + tarot["name"]

        full_prompt = f"{self.prompt}\n\n問題：{problem}\n塔羅牌：{card_name}\n相關詞：{related}\n"

        return full_prompt, card_name, img_path

    def get_single_tarot(self):
        i, r = self._get_tarot_info()
        return self._get_tarot_msg_path(i, r)

    def _get_tarot_msg_path(self, i, r):
        msg = self._get_tarot_msg(i, r)
        path = self._get_tarot_path(i, r)
        return msg, path

    def get_tarots(self, n):
        if n > 156:
            n = 156
        if n < 1:
            n = 1
        arr = list(range(78 * 2))
        random.shuffle(arr)
        for i in range(n):
            yield self._get_tarot_msg_path(arr[i] // 2, arr[i] % 2)

    def _get_tarot_info(self):
        ri = random.randint(0, 77)
        rr = random.randint(0, 1)
        return ri, rr

    def _get_tarot_path(self, i, r):
        return "./tarot/%02d%s.jpg" % (i, "r" if r else "")

    def _get_tarot_msg(self, i, r):
        tarot = self.tarot["%02d" % i]
        card = tarot[KEY_REVERSED[r]]
        msg = "**%s%s**\n\n" % (STR_REVERSED[r], tarot["name"])
        msg += self._parse_result_detail(card)
        logger.info("Response %s%s" % (STR_REVERSED[r], tarot["name"]))
        return msg

    def _parse_result_detail(self, r):
        rtn = list()
        for k in DETAIL_ORDER:
            rtn.append("**%s**\n%s" % (STR_COLUMN[k], r[k]))
        return "\n\n".join(rtn)

    def _init_query_dict(self):
        self.query = dict()
        card_name = list()
        for idx in self.tarot:
            name = self.tarot[idx]["name"]
            self.query[name] = int(idx)
            card_name.append(name)
        self.query_pattern = re.compile("(%s)" % "|".join(card_name))

    def is_reversed(self, term):
        if "反" in term:
            return 1
        if "逆" in term:
            return 1
        return 0

    def query_card(self, query):
        try:
            query_card = self.query_pattern.findall(query)[0]
            query_dir = self.is_reversed(query)
            return self._get_tarot_msg_path(self.query[query_card], query_dir)
        except:
            sim_name = self.calc_similarity(query)
            return "找不到**%s**這張牌，你是指**%s**嗎?" % (query, sim_name), None

    def calc_similarity(self, query):
        names = ["正向正位" + val["name"] for val in self.tarot.values()]
        names += ["反向反位" + val["name"] for val in self.tarot.values()]
        max_sim, max_name = float("-inf"), ""
        for name in names:
            sim = self.sim(name, query)
            if sim > max_sim:
                max_sim = sim
                max_name = name
        return max_name[4:]

    def sim(self, q1, q2):
        s1 = set(q1)
        s2 = set(q2)
        a = len(s1 & s2)
        b = len(s1 | s2)
        return a / b
