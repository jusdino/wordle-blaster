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
        self.assertEqual(wordle.state['rowIndex'], len([x for x in blaster.constraints['guesses']]))
        for guess in wordle.state['boardState'][:wordle.state['rowIndex']]:
            self.assertIn(guess, blaster.constraints['guesses'])

    def test_voice(self):
        """Known error case, reproduced based on logs"""
        from wordle import SimWordle
        from blaster.basic import BasicWordleBlaster

        wordle = SimWordle(solution='voice')
        word = 'click'
        blaster = BasicWordleBlaster(wordle)
        result = wordle.submit_guess(word)
        expected_result = ['absent', 'absent', 'correct', 'correct', 'absent']
        self.assertEqual(expected_result, result)
        blaster.process_result(word, expected_result)

        candidates = blaster.get_candidate_words()
        self.assertGreaterEqual(len(candidates), 1)

    def test_moist(self):
        """Known error case, reproduced based on logs"""
        from wordle import SimWordle
        from blaster.basic import BasicWordleBlaster

        wordle = SimWordle(solution='moist')
        blaster = BasicWordleBlaster(wordle)

        word = 'nucha'
        result = wordle.submit_guess(word)
        expected_result = ['absent', 'absent', 'absent', 'absent', 'absent']
        self.assertEqual(expected_result, result)
        blaster.process_result(word, expected_result)

        word = 'tryst'
        result = wordle.submit_guess(word)
        expected_result = ['absent', 'absent', 'absent', 'correct', 'correct']
        self.assertEqual(expected_result, result)
        blaster.process_result(word, expected_result)

        candidates = blaster.get_candidate_words()
        self.assertGreaterEqual(len(candidates), 1)
