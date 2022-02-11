import logging
import os
from unittest import TestCase
import importlib
import pkgutil
import inspect

from wordle import SimWordle
from blaster.basic import BasicWordleBlaster
import blaster


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
        solutions = SimWordle.get_solutions()

        guesses = 0
        for solution in solutions:
            wordle = SimWordle(solution=solution)
            blaster = BlasterCls(wordle)
            blaster.solve()
            guesses += wordle.state['rowIndex']
        guesses /= len(solutions)
        print(f'{BlasterCls.__name__} averaged {guesses:.2f} guesses')
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
