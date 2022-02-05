#!/bin/env python3
import os
import sys
import logging

import requests

from wordle import SimWordle
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
    discord_url = sys.argv[2]
    # wordle = SimWordle()
    # blaster = BasicWordleBlaster(wordle)
    blaster = BasicWordleBlaster()
    blaster.solve()
    logger.info('Posting result')

    # Slack webhook
    summary = blaster.wordle.get_share_summary()
    slack_message = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": summary + "<https://github.com/jusdino/wordle-blaster|What is this?>"
                }
            }
        ]
    }

    resp = requests.post(slack_url, json=slack_message)
    logger.info('Slack returned %s: %s', resp.status_code, resp.text)

    # Discord webhook
    discord_message = summary + "[What is this?](<https://github.com/jusdino/wordle-blaster>)"
    requests.post(discord_url, json={'content': discord_message})
