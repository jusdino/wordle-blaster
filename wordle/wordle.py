import logging
import os
import time

from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from wordle.abstract_wordle import AbstractWordle


logging.basicConfig()
logger = logging.getLogger(__name__)
if os.environ.get('DEBUG', '').lower() == 'true':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


def _get_game_state(driver: webdriver.Firefox):
    logger.debug('Updating state...')
    return driver.execute_script('return JSON.parse(window.localStorage.gameState)')


def _has_board_state(driver: webdriver.Firefox):
    return 'boardState' in _get_game_state(driver)


class _HasGuess():
    def __init__(self, guess: str):
        self.guess = guess

    def __call__(self, driver: webdriver.Firefox):
        game_state = _get_game_state(driver)
        try:
            last_guess = [guess for guess in game_state['boardState'] if guess != ''][-1]
        except IndexError:
            last_guess = ''
        logger.debug('Last guess in game state: "%s"', last_guess)
        return self.guess == last_guess


class Wordle(AbstractWordle):
    def __init__(self, headless: bool = False):
        super().__init__()
        logger.info('Starting firefox...')
        options = webdriver.FirefoxOptions()
        options.headless = headless
        self.driver = webdriver.Firefox(options=options)
        logger.info('Loading wordle...')
        self.driver.get('https://www.powerlanguage.co.uk/wordle/')
        self.wait = WebDriverWait(self.driver, 10, ignored_exceptions=(JavascriptException,))
        self.wait.until(_has_board_state)
        self.body = self.driver.find_element_by_tag_name('body')
        self.body.click()
        self._update_state()
        logger.info('Wordle is ready!')

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

    def _update_state(self):
        state = _get_game_state(self.driver)
        self._state = state

    def submit_guess(self, guess: str) -> list:
        guess = guess.strip()
        logger.debug('Submitting guess, "%s"', guess)
        self.body.send_keys(guess)
        self.body.send_keys(Keys.RETURN)
        self.wait.until(_HasGuess(guess))
        self._update_state()
        time.sleep(6)  # There is no state we can wait on, but Wordle won't accept new submissions for a bit
        return self._state['evaluations'][self._state['rowIndex']-1]
