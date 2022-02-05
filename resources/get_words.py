#!/usr/bin/env python3
"""
Use the unix dictionary words to compile a list of simple 5-letter words

Note: It is better to actually get the list of words out of the wordle source, since there are some discrepancies
in the dictionaries otherwise, and wordle will refuse to accept some of our words.
"""
import os
import re
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)
if os.environ.get('DEBUG', '').lower() == 'true':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


all_ascii = re.compile(r'[a-z]*')


def desireable(word: str):
    if len(word) != 5:
        return False
    if not re.fullmatch(all_ascii, word):
        return False
    return True


def condition(word: str):
    return word.strip().lower()


if __name__ == '__main__':
    with open('/usr/share/dict/words', 'r') as words_in:
        with open('../words.txt', 'w') as words_out:
            for word in words_in:
                word = condition(word)
                logger.debug('Checking word, "%s"', word)
                if desireable(word):
                    logger.info('Found desireable word, "%s"', word)
                    words_out.write(f'{word}\n')
