#!/bin/env python3

import os
from random import choice
import logging

from wordle.abstract_wordle import AbstractWordle
from wordle import Wordle, SimWordle
from wordle.enums import GameStatus


logger = logging.getLogger(__name__)
if os.environ.get('DEBUG', '').lower() == 'true':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


class BasicWordleBlaster():
    """
    Base class that takes care of the administrative details of playing a Wordle

    Subclass this to implement your own custom algorithm
    """
    def __init__(self, wordle: AbstractWordle = None):
        self.wordle = wordle or Wordle(headless=True)
        self.words = self.wordle.get_words()
        self.candidates = set(self.words)
        logger.debug('Wordle created and ready')

    def solve(self):
        logger.info('Here we go!')
        for i in range(6):
            logger.info('%s candidate words remain', len(self.candidates))
            word = self.choose_next_guess()
            logger.info('Guessing word, "%s"', word)
            result = self.wordle.submit_guess(word)
            logger.info('Result: %s', result)
            self.process_result(word, result)
            if self.wordle.state['gameStatus'] == GameStatus.WIN:
                logger.info('I WIN!')
                return
        logger.info('Oh no...')

    def choose_next_guess(self) -> str:
        """
        Override this method to customize your Blaster algorithm

        Default behavior: choose a random word from candidates
        :return: Next guess word
        :rtype: str
        """
        return choice(tuple(self.candidates))

    def process_result(self, word: str, result: int) -> None:
        self.candidates = {
            w for w in self.candidates
            if SimWordle.evaluate_guess(word, w) == result
        }
