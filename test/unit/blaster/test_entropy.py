from unittest import TestCase
import logging
from blaster.entropy import EntropyBlaster

from wordle.enums import Evaluation
from wordle.sim_wordle import SimWordle


logger = logging.getLogger(__name__)


class TestEntropyBlaster(TestCase):
    def test_get_evaluation_hash(self):
        from blaster.entropy import EntropyBlaster

        self.assertEqual(97, EntropyBlaster.get_evaluation_hash(
            [Evaluation.ABSENT, Evaluation.PRESENT, Evaluation.CORRECT, Evaluation.ABSENT, Evaluation.PRESENT]
        ))

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
        logger.info('Test score was %s', score)

    def test_score_guess(self):
        candidates = SimWordle.get_words()[:100]
        e_information = EntropyBlaster.score_guess('tarps', candidates)
        self.assertGreater(e_information, 0)
        logger.info('Expected information was %s', e_information)

    def test_choose_from_candidates(self):
        from blaster.entropy import EntropyBlaster

        # Trim down the dictionary to save some compute
        words = SimWordle.get_words()[:100]
        candidates = words[-20:]
        solution = words[15]
        logger.info('Test solution is %s', solution)

        wordle = SimWordle(solution=solution)
        wordle.get_words = lambda: words
        blaster = EntropyBlaster(wordle)

        guess = blaster.choose_from_candidates(candidates)
        logger.info('Chosen word was %s', guess)
