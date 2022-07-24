from unittest import TestCase

from wordle.enums import GameStatus


class TestBlaster(TestCase):
    def test_solve(self):
        from wordle import SimWordle
        from blaster.basic import BasicWordleBlaster

        wordle = SimWordle()
        blaster = BasicWordleBlaster(wordle)
        blaster.solve()

        self.assertNotEqual(GameStatus.IN_PROGRESS, wordle.state['gameStatus'])
        self.assertGreater(wordle.state['rowIndex'], 1)

    def test_voice(self):
        """Known error case, reproduced based on logs"""
        from wordle import SimWordle
        from blaster.basic import BasicWordleBlaster

        wordle = SimWordle(solution='voice')
        word = 'click'
        blaster = BasicWordleBlaster(wordle)
        result = wordle.submit_guess(word)
        expected_result = SimWordle.get_evaluation_hash(['absent', 'absent', 'correct', 'correct', 'absent'])
        self.assertEqual(expected_result, result)
        blaster.process_result(word, expected_result)

        self.assertGreaterEqual(len(blaster.candidates), 1)

    def test_moist(self):
        """Known error case, reproduced based on logs"""
        from wordle import SimWordle
        from blaster.basic import BasicWordleBlaster

        wordle = SimWordle(solution='moist')
        blaster = BasicWordleBlaster(wordle)

        word = 'nucha'
        result = wordle.submit_guess(word)
        expected_result = SimWordle.get_evaluation_hash(['absent', 'absent', 'absent', 'absent', 'absent'])
        self.assertEqual(expected_result, result)
        blaster.process_result(word, expected_result)

        word = 'tryst'
        result = wordle.submit_guess(word)
        expected_result = SimWordle.get_evaluation_hash(['absent', 'absent', 'absent', 'correct', 'correct'])
        self.assertEqual(expected_result, result)
        blaster.process_result(word, expected_result)

        self.assertGreaterEqual(len(blaster.candidates), 1)
