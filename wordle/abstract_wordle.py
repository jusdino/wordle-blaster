from abc import ABC, abstractmethod, abstractproperty

from wordle.enums import Evaluation, GameStatus


class AbstractWordle(ABC):
    _evaluation_map = {
        Evaluation.ABSENT: "⬛",
        Evaluation.PRESENT: "🟨",
        Evaluation.CORRECT: "🟩"
    }

    def __init__(self):
        self._state = {'gameStatus': GameStatus.IN_PROGRESS}

    @property
    def state(self):
        # Not that the copy here provides some little protection against
        # mutation by the user of this interface, but only at the top level.
        state = self._state.copy()
        # I just can't stand to hand the solution to the blaster
        state.pop('solution')
        return state

    @abstractmethod
    def submit_guess(self, guess: str) -> list:
        pass

    def get_share_summary(self):
        if self._state['gameStatus'] == GameStatus.IN_PROGRESS:
            raise RuntimeError('Cannot get state for a game that is in progress')
        tries = self._state['rowIndex'] if self._state['gameStatus'] == GameStatus.WIN else 'X'
        report = f'Wordle {tries}/6\n'
        for i in range(self._state['rowIndex']):
            for e in self._state['evaluations'][i]:
                report += self._evaluation_map[e]
            report += '\n'
        return report
