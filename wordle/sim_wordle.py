from random import choice

from .enums import Evaluation, GameStatus
from .abstract_wordle import AbstractWordle


class SimWordle(AbstractWordle):
    _evaluation_cache = {}

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

    def submit_guess(self, guess: str) -> int:
        super().submit_guess(guess)
        if self._state['gameStatus'] != GameStatus.IN_PROGRESS:
            raise RuntimeError('This game is no longer in progress!')
        return self._evaluate_and_update(guess)

    def _evaluate_and_update(self, guess: str) -> int:
        evaluation = self.evaluate_guess(guess, self._state['solution'])

        self._state['boardState'][self._state['rowIndex']] = guess
        self._state['evaluations'][self._state['rowIndex']] = evaluation
        self._state['rowIndex'] += 1
        if guess == self._state['solution']:
            self._state['gameStatus'] = GameStatus.WIN
        elif self._state['rowIndex'] > 5:
            self._state['gameStatus'] = GameStatus.FAIL
        return evaluation

    @classmethod
    def evaluate_guess(cls, guess: str, solution: str) -> int:
        """
        Return evaluation of guess.
        Note: The case of double-letter words is handled specially and I'm not positive on
        the details. It appears that evaluations for any given letter are awarded in a best
        first result order, meaning that in the case of double guess letters, the CORRECT
        result will take precedence over the PRESENT result, and any given solution letter
        only 'awards' a positive evaluation once.
        """
        try:
            return cls._evaluation_cache[solution][guess]
        except KeyError:
            pass
        solution_list = [letter for letter in solution]
        evaluation_list = [Evaluation.ABSENT]*5
        # Find all CORRECT results first
        for i, letter in enumerate(guess):
            if solution_list[i] == letter:
                solution_list[i] = None
                evaluation_list[i] = Evaluation.CORRECT
        # Then find PRESENT results
        for i, letter in enumerate(guess):
            if evaluation_list[i] == Evaluation.ABSENT:
                try:
                    match_idx = solution_list.index(letter)
                    solution_list[match_idx] = None
                    evaluation_list[i] = Evaluation.PRESENT
                except ValueError:
                    pass

        # Cache evaluations to save some compute
        result = cls.get_evaluation_hash(evaluation_list)
        guesses = cls._evaluation_cache.get(solution, {})
        guesses[guess] = result
        cls._evaluation_cache[solution] = guesses
        return result
