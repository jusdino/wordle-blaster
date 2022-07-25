from abc import ABC, abstractmethod
import importlib
from typing import Tuple, List

from wordle.enums import Evaluation, GameStatus
from wordle import resources


class AbstractWordle(ABC):
    _evaluation_map = {
        Evaluation.ABSENT: "⬛",
        Evaluation.PRESENT: "🟨",
        Evaluation.CORRECT: "🟩"
    }

    @staticmethod
    def get_words() -> Tuple[str]:
        """
        A convenience method to get the official tuple of valid words
        """
        with importlib.resources.as_file(importlib.resources.files(resources).joinpath('words.txt')) as path:
            with open(path, 'r') as f:
                return tuple(word.strip() for word in f)

    @staticmethod
    def get_solutions():
        """
        A convenience method to get the official tuple of potential solutions
        """
        with importlib.resources.as_file(importlib.resources.files(resources).joinpath('solutions.txt')) as path:
            with open(path, 'r') as f:
                return tuple(word.strip() for word in f)

    def __init__(self):
        self._state = {'gameStatus': GameStatus.IN_PROGRESS}

    @property
    def state(self):
        """
        Get a copy of the game state from the wordle
        """
        # Note that the copy here provides some little protection against
        # mutation by the user of this interface, but only at the top level.
        state = self._state.copy()
        # I just can't stand to hand the solution to the blaster
        state.pop('solution')
        return state

    @abstractmethod
    def submit_guess(self, guess: str) -> int:
        """
        Submit a guess word to the wordle, recieve an evaluation back
        """
        pass

    def get_game_solution_number(self):
        solution = self._state['solution']
        return self.get_solutions().index(solution)

    def get_share_summary(self):
        if self._state['gameStatus'] == GameStatus.IN_PROGRESS:
            raise RuntimeError('Cannot get state for a game that is in progress')
        solution_number = self.get_game_solution_number()
        tries = self._state['rowIndex'] if self._state['gameStatus'] == GameStatus.WIN else 'X'
        report = f'{self.__class__.__name__} {solution_number} {tries}/6\n'
        for i in range(self._state['rowIndex']):
            for e in self._state['evaluations'][i]:
                report += self._evaluation_map[e]
            report += '\n'
        return report

    @staticmethod
    def get_evaluation_hash(evaluation: List[str]) -> int:
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
