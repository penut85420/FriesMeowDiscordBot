from fries.trpg.dice import Dice, DiceFormatError, DiceRangeError
import unittest
import sys
sys.path.append('.')


class DiceTest(unittest.TestCase, Dice):
    def test_roll(self):
        self.assertRegex(Dice.roller('1d99'), r'^\d+$')
        self.assertRegex(Dice.roller('3d99'), r'^\d+ \+ \d+ \+ \d+ = \d+$')
        self.assertRegex(
            Dice.roller('3d99+66'),
            r'^\(\d+ \+ \d+ \+ \d+\) \+ \d+ = [\d]+$')
        self.assertRegex(Dice.roller('1d99', 'Cool'), r'^投擲 Cool 的結果是 \d+$')
        self.assertRegex(
            Dice.roller('2d99', 'Cute'),
            r'^投擲 Cute 的結果是 \d+ \+ \d+ = \d+$')
        self.assertRegex(
            Dice.roller('3d100', 'Passion'),
            r'^投擲 Passion 的結果是 \d+ \+ \d+ \+ \d+ = \d+$')
        self.assertEqual(Dice.roller('51d100'), '第 1 個參數超過最大值 50')
        self.assertEqual(Dice.roller('50d1001'), '第 2 個參數超過最大值 1000')
        self.assertEqual(Dice.roller('50d1000+100000'), '第 3 個參數超過最大值 99999')
        self.assertEqual(
            Dice.roller('3dd6'),
            '格式必須是 NdM 或 NdM+K，例如 `!dice 2d6` 是投擲兩顆六面的骰子')

    def test_parse(self):
        self.assertEqual(self._parse('3d6'), (3, 6, 0, '', 0))
        self.assertEqual(self._parse('3d6+9'), (3, 6, 9, '+', 0))
        self.assertEqual(self._parse('99999d6+9'), (99999, 6, 9, '+', 0))
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
