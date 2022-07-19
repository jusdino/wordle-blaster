#!/bin/env python3

from copy import deepcopy
import os
from random import choice
import logging
from typing import Tuple

from wordle.abstract_wordle import AbstractWordle
from wordle import Wordle
from wordle.enums import Evaluation, GameStatus


logger = logging.getLogger(__name__)
if os.environ.get('DEBUG', '').lower() == 'true':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


class BasicWordleBlaster():
    """
    Start with the most intuitive (first) strategy I can think of: random choice of possible words
    """
    def __init__(self, wordle: AbstractWordle = None):
        self.constraints = {
            'present': set(),
            'absent': set(),
            'correct': [None, None, None, None, None],
            'incorrect': [set(), set(), set(), set(), set()],
            'guesses': set()
        }
        self.wordle = wordle or Wordle(headless=True)
        self.words = self.wordle.get_words()
        logger.debug('Wordle created and ready')

    def __del__(self):
        if hasattr(self, 'words_file'):
            self.words_file.close()

    def solve(self):
        logger.info('Here we go!')
        for i in range(6):
            word = self.get_candidate_word()
            logger.info('Guessing word, "%s"', word)
            result = self.wordle.submit_guess(word)
            logger.info('Result: %s', result)
            self.process_result(word, result)
            if self.wordle.state['gameStatus'] == GameStatus.WIN:
                logger.info('I WIN!')
                return
        logger.info('Oh no...')

    def get_candidate_words(self) -> Tuple[str]:
        return tuple(
            word for word in self.words
            if self.check_word(word)
        )

    def get_candidate_word(self) -> str:
        candidates = self.get_candidate_words()
        logger.info('Choosing from %s candidate words', len(candidates))
        return self.choose_from_candidates(candidates)

    def choose_from_candidates(self, candidates: tuple) -> str:
        return choice(candidates)

    def check_word(self, word: str) -> bool:
        return self.check_word_with_constraints(word, self.constraints)

    @staticmethod
    def check_word_with_constraints(word: str, constraints: dict) -> bool:
        for i, correct in enumerate(constraints['correct']):
            if correct is not None and word[i] != correct:
                return False
        for absent in constraints['absent']:
            if absent in word:
                return False
        for present in constraints['present']:
            if present not in word:
                return False
        for i, incorrects in enumerate(constraints['incorrect']):
            if word[i] in incorrects:
                return False
        return word not in constraints['guesses']

    def process_result(self, word: str, result: list) -> None:
        self.constraints = self.process_result_with_constraints(
            guess=word,
            result=result,
            constraints=self.constraints
        )

    @staticmethod
    def process_result_with_constraints(guess: str, result: list, constraints: dict) -> dict:
        constraints = deepcopy(constraints)
        constraints['guesses'].add(guess)
        for i, evaluation in enumerate(result):
            if evaluation == Evaluation.CORRECT:
                constraints['present'].add(guess[i])
                constraints['correct'][i] = guess[i]
        for i, evaluation in enumerate(result):
            if evaluation == Evaluation.PRESENT:
                constraints['present'].add(guess[i])
                constraints['incorrect'][i].add(guess[i])
            elif evaluation == Evaluation.ABSENT:
                # In the case of a double-letter, wordle will evaluate the second
                # as absent, so we have to handle that case here
                if guess[i] not in constraints['present']:
                    constraints['absent'].add(guess[i])
        return constraints
