import re
import random
import unittest

class DiceFormatError(Exception):
    def __str__(self):
        return '格式必須是 NdM 或 NdM+K'

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
    DICE_PATTERN = re.compile('^([0-9]+)d([0-9]+)\\+?([0-9]*)$', re.I)

    def __init__(self, dice, name=None):
        self.name = name
        self.roll(dice)
    
    def roll(self, dice):
        a, b, c = self._parse(dice)
        self._check_all_range(a, b, c)
        self.dseq = self._gen_dice_sequence(a, b)
        if c: self.dseq.append(c)
        self.total = sum(self.dseq) + c

    def _parse(self, dice):
        try:
            a, b, c = Dice.DICE_PATTERN.findall(dice)[0]
        except IndexError:
            raise DiceFormatError()
        a = int(a)
        b = int(b)
        c = c or 0
        c = int(c)
        return a, b, c
    
    def _check_range(self, num, n=0, max_bound=MAX_BOUND, min_bound=MIN_BOUND):
        if num < min_bound: raise DiceRangeError(n, min_bound, False)
        if num > max_bound: raise DiceRangeError(n, max_bound, True)
        return True
    
    def _check_all_range(self, a, b, c):
        if not self._check_range(a, 1, max_bound=50): return False
        if not self._check_range(b, 2): return False
        if not self._check_range(c, 3, min_bound=0, max_bound=99999): return False
        return True

    def _gen_dice_sequence(self, a, b):
        return [random.randint(1, b) for _ in range(a)]

    def __str__(self):
        msg = str()
        if self.name:
            msg = '投擲 %s 的結果是 ' % self.name

        if len(self.dseq) == 1:
            msg += str(self.total)
        else:
            msg += '%s = %d' % (' + '.join([str(d) for d in self.dseq]), self.total)
        return msg
    
    @staticmethod
    def roller(dice, name=None):
        try:
            return str(Dice(dice, name))
        except Exception as e:
            return str(e)

class DiceTest(unittest.TestCase, Dice):
    def test_roll(self):
        self.assertRegex(Dice.roller('1d99'), r'^\d+$')
        self.assertRegex(Dice.roller('3d99'), r'^\d+ \+ \d+ \+ \d+ = \d+$')
        self.assertRegex(Dice.roller('3d99+66'), r'^\d+ \+ \d+ \+ \d+ \+ \d+ = [\d]+$')
        self.assertRegex(Dice.roller('1d99', 'Cool'), r'^投擲 Cool 的結果是 \d+$')
        self.assertRegex(Dice.roller('2d99', 'Cute'), r'^投擲 Cute 的結果是 \d+ \+ \d+ = \d+$')
        self.assertRegex(Dice.roller('3d100', 'Passion'), r'^投擲 Passion 的結果是 \d+ \+ \d+ \+ \d+ = \d+$')
        self.assertEqual(Dice.roller('51d100'), '第 1 個參數超過最大值 50')
        self.assertEqual(Dice.roller('50d1001'), '第 2 個參數超過最大值 1000')
        self.assertEqual(Dice.roller('50d1000+100000'), '第 3 個參數超過最大值 99999')
        self.assertEqual(Dice.roller('3dd6'), '格式必須是 NdM 或 NdM+K')

    def test_parse(self):
        self.assertEqual(self._parse('3d6'), (3, 6, 0))
        self.assertEqual(self._parse('3d6+9'), (3, 6, 9))
        self.assertEqual(self._parse('99999d6+9'), (99999, 6, 9))
        self.assertRaises(DiceFormatError, self._parse, dice='3d-6+9')
        self.assertRaises(DiceFormatError, self._parse, dice='3.3d6+9')

    def test_check_range(self):
        self.assertTrue(self._check_range(1000))
        self.assertTrue(self._check_range(999))
        self.assertTrue(self._check_range(50, max_bound=50))
        self.assertRaises(DiceRangeError, self._check_range, 51, max_bound=50)
        self.assertRaises(DiceRangeError, self._check_range, 0, min_bound=51)
        self.assertRaises(DiceRangeError, self._check_range, 1001)
        self.assertRaises(DiceRangeError, self._check_range, 0)
        self.assertRaises(DiceRangeError, self._check_range, -1)

if __name__ == '__main__':
    unittest.main()