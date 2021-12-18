from fries.easy_calculator import EasyCalculator
from unittest import TestCase
import sys
sys.path.append('.')


class EasyCalculatorTest(TestCase):
    def test_calc(self):
        ec = EasyCalculator()
        data = [
            ('1+2-3', '計算結果：1 + 2 - 3 = 0'),
            ('(1-(2   + 3)*4)/ 5', '計算結果：(1 - (2 + 3) * 4) / 5 = -3.8'),
            ('1e+5*3.14', '計算結果：1e+5 * 3.14 = 314000.0'),
            ('a+b', '不是個簡易運算式，只能包含數字和 + - * / %'),
            ('(1-(2   + 3)*4)/ 5)', '格式錯誤的運算式'),
            ('9**9', '不允許指數運算！'),
            ('9* *9', '格式錯誤的運算式'),
            ('9 / (3-(2+1))', '算式出現除以零的行為'),
        ]
        for expr, result in data:
            self.assertEqual(ec.calc(expr), result)
