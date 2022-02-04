#!/bin/env python3
import os
from random import choice
import logging

from wordle.abstract_wordle import AbstractWordle
from wordle import Wordle
from wordle.enums import Evaluation, GameStatus


logging.basicConfig()
logger = logging.getLogger(__name__)
if os.environ.get('DEBUG', '').lower() == 'true':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


class BasicWordleBlaster():
    """
    Start with the most intuitive (first) strategy I can think of
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
        self.words_file = open(os.path.join('resources', 'words.txt'), 'r')
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

    def get_candidate_word(self) -> str:
        self.words_file.seek(0)
        candidates = tuple(
            word.strip() for word in self.words_file
            if self.check_word(word)
        )
        logger.info('Choosing from %s candidate words', len(candidates))
        return self.choose_from_candidates(candidates)

    def choose_from_candidates(self, candidates: tuple) -> str:
        return choice(candidates)

    def check_word(self, word: str) -> bool:
        for i, correct in enumerate(self.constraints['correct']):
            if correct is not None and word[i] != correct:
                return False
        for absent in self.constraints['absent']:
            if absent in word:
                return False
        for present in self.constraints['present']:
            if present not in word:
                return False
        for i, incorrects in enumerate(self.constraints['incorrect']):
            if word[i] in incorrects:
                return False
        return word not in self.constraints['guesses']

    def process_result(self, word: str, result: list) -> None:
        self.constraints['guesses'].add(word)
        for i, evaluation in enumerate(result):
            if evaluation == Evaluation.CORRECT:
                self.constraints['present'].add(word[i])
                self.constraints['correct'][i] = word[i]
            elif evaluation == Evaluation.PRESENT:
                self.constraints['present'].add(word[i])
                self.constraints['incorrect'][i].add(word[i])
            elif evaluation == Evaluation.ABSENT:
                # In the case of a double-letter, wordle will evaluate the second
                # as absent, so we have to handle that case here
                if word[i] not in self.constraints['present']:
                    self.constraints['absent'].add(word[i])
