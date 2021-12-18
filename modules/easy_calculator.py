import re


class EasyCalculator:
    def __init__(self):
        self.legal = re.compile(r'^[\.\de\+\-\*/% \(\)]*$')
        symbol_list = [
            '[\d]+e[\+\-][\d]+', '[\d\.]+',
            '\+', '\-', '\*', '/', '%', '\(', '\)'
        ]
        self.symbol = re.compile('(%s)' % '|'.join(symbol_list))

    def calc(self, expr):
        try:
            self._is_easy(expr)
            self._no_exp(expr)
            self._is_calculable(expr)
            return '計算結果：%s = %s' % (self._pretty_expr(expr), str(eval(expr)).upper())
        except Exception as e:
            return str(e)

    def _pretty_expr(self, expr):
        result = self.symbol.findall(expr)
        return ' '.join(result).replace('( ', '(').replace(' )', ')')

    def _is_easy(self, expr):
        if self.legal.match(expr) is None:
            raise EasyCalculator.NotEasyExpression()
        return True

    def _no_exp(self, expr):
        if '**' in expr:
            raise EasyCalculator.ExponentNotAllowed()
        return True

    def _is_calculable(self, expr):
        try:
            exec(expr)
            return True
        except ZeroDivisionError:
            raise EasyCalculator.DividByZero()
        except:
            raise EasyCalculator.NotCalculable()

    class NotEasyExpression(Exception):
        def __str__(self):
            return '不是個簡易運算式，只能包含數字和 + - * / %'

    class ExponentNotAllowed(Exception):
        def __str__(self):
            return '不允許指數運算！'

    class NotCalculable(Exception):
        def __str__(self):
            return '格式錯誤的運算式'

    class DividByZero(Exception):
        def __str__(self):
            return '算式出現除以零的行為'


if __name__ == "__main__":
    EC = EasyCalculator()
    print(EC.calc('1e+5*3.14'))
    # s = '3e-5'
    # p = '[\d]+e[\+\-][\d]+'
    # print(re.search(p, s))
