from unittest import TestCase
import logging
from blaster.entropy import EntropyBlaster

from wordle.sim_wordle import SimWordle


logger = logging.getLogger(__name__)


class TestEntropyBlaster(TestCase):
    def test_get_guess_result_counts(self):
        from blaster.entropy import EntropyBlaster

        wordle = SimWordle(solution='words')
        blaster = EntropyBlaster(wordle)

        candidates = blaster.words[:100]
        results = blaster._get_guess_result_counts('guess', candidates)
        self.assertEqual(100, sum(results.values()))

    def test_sum_expected_information(self):
        from blaster.entropy import EntropyBlaster

        results = {
            0: 1,
            1: 3,
            2: 2,
            4: 1
        }
        score = EntropyBlaster._sum_expected_information(results, 7)
        self.assertGreater(score, 0)
        logger.info('Test score was %.4f', score)

    def test_score_guess(self):
        candidates = SimWordle.get_words()[:100]
        e_information = EntropyBlaster.score_guess('tarps', candidates)
        self.assertGreater(e_information, 0)
        logger.info('Expected information was %.4f', e_information)

    def test_choose_next_guess(self):
        from blaster.entropy import EntropyBlaster

        # Trim down the dictionary to save some compute
        words = SimWordle.get_words()[:100]
        solution = words[15]
        logger.info('Test solution is %s', solution)

        wordle = SimWordle(solution=solution)
        wordle.get_words = lambda: words
        blaster = EntropyBlaster(wordle)
        blaster.candidates = set(words[-20:])

        guess = blaster.choose_next_guess()
        logger.info('Chosen word was %s', guess)
