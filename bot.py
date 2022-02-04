#!/bin/env python3
import os
import sys
import logging

import requests

from blaster import BasicWordleBlaster


logging.basicConfig()
logger = logging.getLogger(__name__)
if os.environ.get('DEBUG', '').lower() == 'true':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


if __name__ == "__main__":
    logger.info('Starting bot...')
    slack_url = sys.argv[1]
    blaster = BasicWordleBlaster()
    blaster.solve()
    logger.info('Posting result')
    requests.post(slack_url, json={'text': blaster.wordle.get_share_summary()})
