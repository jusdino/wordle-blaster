from unittest import TestCase

from wordle.enums import GameStatus


class TestBlaster(TestCase):
    def setUp(self):
        from wordle import SimWordle
        from blaster.basic import BasicWordleBlaster

        self.wordle = SimWordle()
        self.blaster = BasicWordleBlaster(self.wordle)

    def test_solve(self):
        self.blaster.solve()

        self.assertNotEqual(GameStatus.IN_PROGRESS, self.wordle.state['gameStatus'])
        self.assertGreater(self.wordle.state['rowIndex'], 1)
        self.assertEqual(self.wordle.state['rowIndex'], len([x for x in self.blaster.constraints['guesses']]))
        for guess in self.wordle.state['boardState'][:self.wordle.state['rowIndex']]:
            self.assertIn(guess, self.blaster.constraints['guesses'])
