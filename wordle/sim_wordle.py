import os
from random import choice

from .enums import Evaluation, GameStatus
from .abstract_wordle import AbstractWordle


class SimWordle(AbstractWordle):
    def __init__(self, *, solution: str = None):
        """
        A simulation of the wordle game for ease of testing
        """
        super().__init__()
        solutions = self.get_solutions()

        if solution is not None:
            # A little validation on the provided solution
            if not isinstance(solution, str) or solution not in self.get_words():
                raise ValueError(f'Expected {solution} to be a str word with 5 letters.')

        self._state = {
            'boardState': ['', '', '', '', '', ''],
            'evaluations': [
                None,
                None,
                None,
                None,
                None,
                None
            ],
            'solution': solution or choice(solutions),
            'gameStatus': GameStatus.IN_PROGRESS,
            'hardMode': False,
            'rowIndex': 0
        }
        self.solution_letter_counts = {}
        for letter in self._state['solution']:
            try:
                self.solution_letter_counts[letter] += 1
            except KeyError:
                self.solution_letter_counts[letter] = 1

    def submit_guess(self, guess: str) -> list:
        super().submit_guess(guess)
        if self._state['gameStatus'] != GameStatus.IN_PROGRESS:
            raise RuntimeError('This game is no longer in progress!')
        return self._evaluate_guess(guess)

    def _evaluate_guess(self, guess: str) -> list:
        """
        Return evaluation of guess.
        Note: The case of double-letter words is handled specially and I'm not positive on
        the details. Best I can guess, the second letter in a double-letter guess word
        will only be evaluated as CORRECT or PRESENT if there is also a second of that
        letter in the solution word. I track the letter counts here to account for that.
        """
        self._state['boardState'][self._state['rowIndex']] = guess
        evaluation = []
        guess_letter_counts = {}
        for i, letter in enumerate(guess):
            try:
                guess_letter_counts[letter] += 1
            except KeyError:
                guess_letter_counts[letter] = 1
            evaluation.append(self._evaluate_letter(i, letter, guess_letter_counts))

        self._state['evaluations'][self._state['rowIndex']] = evaluation
        self._state['rowIndex'] += 1
        if guess == self._state['solution']:
            self._state['gameStatus'] = GameStatus.WIN
        elif self._state['rowIndex'] > 5:
            self._state['gameStatus'] = GameStatus.FAIL
        return evaluation

    def _evaluate_letter(self, idx: int, letter: str, guess_letter_counts: dict) -> str:
        # Force ABSENT for possible repeat letters that outnumber repeats in the solution
        if guess_letter_counts[letter] <= self.solution_letter_counts.get(letter, 0):
            if letter == self._state['solution'][idx]:
                return Evaluation.CORRECT
            if letter in self._state['solution']:
                return Evaluation.PRESENT
        return Evaluation.ABSENT
