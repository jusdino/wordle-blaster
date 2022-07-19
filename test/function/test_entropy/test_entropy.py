from unittest import TestCase
import logging

from blaster.entropy import EntropyBlaster
from wordle import SimWordle
from wordle.enums import GameStatus


logger = logging.getLogger(__name__)


class TestEntropyBlaster(TestCase):
    def test_solve(self):
        # Trim down the dictionary to save some compute
        words = SimWordle.get_words()[:100]
        candidates = words[-20:]
        solution = words[15]
        logger.info('Test solution is %s', solution)

        wordle = SimWordle(solution=solution)
        wordle.get_words = lambda: words

        blaster = EntropyBlaster(wordle)
        blaster.solve()
        logger.debug(wordle.state)
        self.assertEqual(GameStatus.WIN, wordle.state['gameStatus'])
