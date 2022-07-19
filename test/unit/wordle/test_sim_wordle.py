from unittest import TestCase

from wordle.sim_wordle import SimWordle


class TestSimWordle(TestCase):
    def test_evaluate_guess(self):
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
                result = SimWordle.evaluate_guess(
                    guess=example[1],
                    solution=example[0]
                )
                self.assertEqual(example[2], result)
