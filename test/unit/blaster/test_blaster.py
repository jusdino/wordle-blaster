from unittest import TestCase
import logging
from blaster.basic import BasicWordleBlaster

from wordle.sim_wordle import SimWordle


logger = logging.getLogger(__name__)


class TestBlaster(TestCase):
    def test_process_results(self):
        words = SimWordle.get_words()[:100]
        solution = words[50]
        wordle = SimWordle(solution=solution)
        wordle.get_words = lambda: words
        blaster = BasicWordleBlaster(wordle=wordle)

        guess = words[49]
        result = SimWordle.evaluate_guess(guess, solution)
        self.assertEqual(len(blaster.candidates), len(words))
        blaster.process_result(guess, result)
        self.assertLess(len(blaster.candidates), len(words))
        self.assertIn(solution, blaster.candidates)
