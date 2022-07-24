from unittest import TestCase

from wordle.abstract_wordle import AbstractWordle
from wordle.enums import Evaluation


class TestAbstractWordle(TestCase):
    def test_get_evaluation_hash(self):
        self.assertEqual(97, AbstractWordle.get_evaluation_hash(
            [Evaluation.ABSENT, Evaluation.PRESENT, Evaluation.CORRECT, Evaluation.ABSENT, Evaluation.PRESENT]
        ))
