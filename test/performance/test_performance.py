import logging
from datetime import datetime
from unittest import TestCase
import importlib
import pkgutil
import inspect

from wordle import SimWordle
from blaster.basic import BasicWordleBlaster
import blaster
from wordle.enums import GameStatus


logger = logging.getLogger(__name__)


class TestPerformance(TestCase):
    """
    Tests each BasicWordleBlaster class/subclass against each known solution word
    and reports its average number of guesses.
    """
    pass


# Test method for each WordleBlaster
def _test_blaster(BlasterCls):
    """
    Wraps test method to provide the BlasterCls
    """
    def test_method(self):
        """
        Solve each possible wordle solution and average the total guesses
        """
        print(f'{BlasterCls.__name__}: Beginning performance test')
        solutions = SimWordle.get_solutions()
        total_solutions = len(solutions)

        total_game_duration = 0
        guesses = 0
        wins = 0
        for i, solution in enumerate(solutions):
            try:
                start_time = datetime.now()
                wordle = SimWordle(solution=solution)
                blaster = BlasterCls(wordle)
                blaster.solve()
                if wordle.state['gameStatus'] == GameStatus.WIN:
                    guesses += wordle.state['rowIndex']
                    wins += 1
                end_time = datetime.now()
                game_duration = (end_time-start_time).total_seconds()
                total_game_duration += game_duration
                logger.info(
                    'Completed wordle %s of %s in %s guesses and in %.3f seconds',
                    i,
                    total_solutions,
                    wordle.state['rowIndex'],
                    game_duration
                )
                logger.info('Mean game duration so far: %.2f seconds', total_game_duration/(i+1))
            except KeyboardInterrupt:
                total_solutions = i+1
                break
        mean_game_duration = total_game_duration/total_solutions
        guesses /= wins
        success_rate = 100*wins/total_solutions
        logger.info('Completed %s wordles', total_solutions)
        logger.info(
            '%s averaged %2f guesses, success rate %.2f%%, mean game duration %.3f seconds',
            BlasterCls.__name__,
            guesses,
            success_rate,
            mean_game_duration
        )
        print(f'{BlasterCls.__name__} completed {total_solutions} wordles')
        print(
            f'{BlasterCls.__name__} averaged {guesses:.2f} guesses, success rate '
            f'{success_rate:.2f}%, mean game time {mean_game_duration:.3f} seconds'
        )
    return test_method


# Search for modules in the blaster namespace package
def _iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


discovered_modules = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in _iter_namespace(blaster)
}


# Iterate through module members, looking for WordleBlasters, adding a test method for each
for module in discovered_modules.values():
    for name, member in inspect.getmembers(module):
        if inspect.isclass(member) and issubclass(member, BasicWordleBlaster):
            # member is a WordleBlaster class
            method_name = f'test_{name}'
            print(f'Discovered {name} for testing')
            setattr(TestPerformance, method_name, _test_blaster(member))
