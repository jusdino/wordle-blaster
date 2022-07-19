#!/bin/env python3
import logging
import os
from math import log
from typing import List, Tuple, Iterable

from wordle import SimWordle
from wordle.enums import Evaluation
from blaster.basic import BasicWordleBlaster


logger = logging.getLogger(__name__)
if os.environ.get('DEBUG', '').lower() == 'true':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


class EntropyBlaster(BasicWordleBlaster):
    """
    This is a simplified approach to a Blaster based on Information Theory
    and inspired by 3blue1brown. See his great description at:
    https://www.youtube.com/watch?v=v68zYyaEmEA&t=666s
    """
    def choose_from_candidates(self, candidates: Tuple[str]) -> str:
        # This sometimes happens when there is a bug - so we raise
        # an error here to be clear what happened.
        if not candidates:
            raise RuntimeError('We ran out of guess candidates!')
        # Hard-coding the first guess, since it takes a lot of compute and is
        # always the same
        if len(candidates) == len(self.words):
            return 'tares'
        # Expected information calc doesn't help when we already
        # know the answer.
        if len(candidates) == 1:
            return candidates[0]
        guesses = []
        for guess in self.words:
            guesses.append((guess, self.score_guess(guess, candidates)))
        best_guess = guesses[0][0]
        best_score = guesses[0][1]
        for guess, score in guesses:
            if score >= best_score:
                best_score = score
                best_guess = guess
                logger.debug('Guess %s has score of %.3f', guess, score)
        return best_guess

    @classmethod
    def score_guess(cls, guess: str, candidates: Tuple[str]) -> float:
        candidate_count = len(candidates)
        results = cls._get_guess_result_counts(guess, candidates)
        return cls._sum_expected_information(results, candidate_count)

    @classmethod
    def _get_guess_result_counts(cls, guess: str, candidates: Tuple[str]) -> dict:
        results = {}
        for candidate in candidates:
            result = SimWordle.evaluate_guess(guess, candidate)
            result_hash = cls.get_evaluation_hash(result)
            results[result_hash] = results.get(result_hash, 0) + 1
        return results

    @staticmethod
    def _sum_expected_information(results: dict, candidate_count: int) -> float:
        score = 0
        for count in results.values():
            probability = count/candidate_count
            information = -log(probability, 2)
            score += probability * information
        return score

    @staticmethod
    def get_evaluation_hash(evaluation: List[Evaluation]) -> int:
        """
        Convert the list of Evaluations into a unique integer hash

        Two bits per evaluation in the list:
        00 = Absent
        01 = Present
        10 = Correct

        Example Evaluation list:
        | Absent | Present | Correct | Absent | Present |
        | 00     | 01      | 10      | 00     | 01      | -> 0001100001 -> 97
        """
        evaluation_map = {
            Evaluation.ABSENT: 0,
            Evaluation.PRESENT: 1,
            Evaluation.CORRECT: 2
        }
        eval_hash = 0
        for e in evaluation:
            eval_hash = eval_hash << 2
            eval_hash = eval_hash | evaluation_map[e]
        return eval_hash
