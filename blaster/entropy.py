#!/bin/env python3
import logging
import os
from math import log
from typing import Tuple

from wordle import SimWordle
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
    def choose_next_guess(self) -> str:
        # This sometimes happens when there is a bug - so we raise
        # an error here to be clear what happened.
        if not self.candidates:
            raise RuntimeError('We ran out of guess candidates!')
        # Hard-coding the first guess, since it takes a lot of compute and is
        # always the same
        if len(self.candidates) == len(self.words):
            return 'tares'
        # Expected information calc doesn't help when we already
        # know the answer.
        if len(self.candidates) == 1:
            return tuple(self.candidates)[0]
        guesses = []
        for guess in self.words:
            guesses.append((guess, self.score_guess(guess, self.candidates)))
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
            results[result] = results.get(result, 0) + 1
        return results

    @staticmethod
    def _sum_expected_information(results: dict, candidate_count: int) -> float:
        score = 0
        for count in results.values():
            probability = count/candidate_count
            information = -log(probability, 2)
            score += probability * information
        return score
