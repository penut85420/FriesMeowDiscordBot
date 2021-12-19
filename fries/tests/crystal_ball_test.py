import random
from fries import CrystalBallMeow
from unittest import TestCase


class CrystalBallMeowTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.crystal_ball_meow = CrystalBallMeow()

    def test_get(self):
        random.seed(2135)
        emojis = [
            'sa', 'ab', 'up', 'clock2', 'u6709',
            'rage', 'clock3', 'fast_forward',
            'house', 'ok_woman'
        ]

        for emoji in emojis:
            self.assertEqual(self.crystal_ball_meow.get(), emoji)
