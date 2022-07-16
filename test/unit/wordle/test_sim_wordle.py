from unittest import TestCase

from wordle.sim_wordle import SimWordle


class TestSimWordle(TestCase):
    def test_submit_guess(self):
        from wordle.enums import Evaluation
        examples = (
            (
                'basic',  # Solution
                'acids',  # Guess
                [
                    Evaluation.PRESENT,
                    Evaluation.PRESENT,
                    Evaluation.PRESENT,
                    Evaluation.ABSENT,
                    Evaluation.PRESENT
                ],  # Result
            ),
            (
                'basic',  # Solution
                'guess',  # Guess
                [
                    Evaluation.ABSENT,
                    Evaluation.ABSENT,
                    Evaluation.ABSENT,
                    Evaluation.PRESENT,
                    Evaluation.ABSENT
                ],  # Result
            ),
            (
                'solid',
                'poles',
                [
                    Evaluation.ABSENT,
                    Evaluation.CORRECT,
                    Evaluation.CORRECT,
                    Evaluation.ABSENT,
                    Evaluation.PRESENT
                ]
            ),
            (
                'voice',
                'click',
                [
                    Evaluation.ABSENT,
                    Evaluation.ABSENT,
                    Evaluation.CORRECT,
                    Evaluation.CORRECT,
                    Evaluation.ABSENT
                ]
            )
        )
        for example in examples:
            with self.subTest(solution=example[0], guess=example[1]):
                wordle = SimWordle(solution=example[0])
                result = wordle.submit_guess(example[1])
                self.assertEqual(example[2], result)
