import random
import re
import unittest


class DiceFormatError(Exception):
    def __str__(self):
        return '格式必須是 NdM 或 NdM+K，例如 `!dice 2d6` 是投擲兩顆六面的骰子'


class DiceRangeError(Exception):
    def __init__(self, n, bound, is_over):
        self.n = n
        self.bound = bound
        self.is_over = is_over

    def __str__(self):
        if self.is_over:
            return '第 %d 個參數超過最大值 %d' % (self.n, self.bound)
        return '第 %d 個參數小於最小值 %d' % (self.n, self.bound)


class Dice:
    MAX_BOUND = 1000
    MIN_BOUND = 1
    DICE_PATTERN = re.compile(r'^(\d+)d(\d+)(\+|\*)?(\d*)\=?(\d*)$', re.I)
    METHODS = {
        '+': lambda a, b: a + b,
        '*': lambda a, b: a * b,
    }
    IS_SUCCESS = {
        True: '...成功！',
        False: '...失敗QQ'
    }

    def __init__(self, dice, name=None):
        self.name = name
        self.result = None
        self.roll(dice)

    def roll(self, dice):
        a, b, c, m, d = self._parse(dice)
        self._check_all_range(a, b, c)
        self.dseq = self._gen_dice_sequence(a, b)
        self.total = sum(self.dseq)
        if m:
            self.total = Dice.METHODS[m](self.total, c)
        if d:
            self.result = self.total <= d
        self.m = m
        self.c = c
        self.d = d

    def _parse(self, dice):
        try:
            a, b, m, c, d = Dice.DICE_PATTERN.findall(dice)[0]
        except IndexError:
            raise DiceFormatError()
        a = int(a)
        b = int(b)
        c = int(c or 0)
        d = int(d or 0)
        return a, b, c, m, d

    def _check_range(self, num, n=0, max_bound=MAX_BOUND, min_bound=MIN_BOUND):
        if num < min_bound:
            raise DiceRangeError(n, min_bound, False)
        if num > max_bound:
            raise DiceRangeError(n, max_bound, True)
        return True

    def _check_all_range(self, a, b, c):
        if not self._check_range(a, 1, max_bound=50):
            return False
        if not self._check_range(b, 2):
            return False
        if not self._check_range(c, 3, min_bound=0, max_bound=99999):
            return False
        return True

    def _gen_dice_sequence(self, a, b):
        return [random.randint(1, b) for _ in range(a)]

    def _join_seq(self):
        return ' + '.join([str(d) for d in self.dseq])

    def _gen_dice_step(self):
        if self.m:
            return '(%s) %s %d = %d' % (
                self._join_seq(), self.m, self.c, self.total)
        return '%s = %d' % (self._join_seq(), self.total)

    def __str__(self):
        msg = list()

        if self.name:
            msg.append('投擲 %s 的結果是 ' % self.name)

        if len(self.dseq) == 1:
            msg.append(str(self.total))
        else:
            msg.append(self._gen_dice_step())

        if self.d:
            msg.append(Dice.IS_SUCCESS[self.result])

        return ''.join(msg)

    @staticmethod
    def roller(dice, name=None):
        try:
            return str(Dice(dice, name))
        except Exception as e:
            return str(e)
