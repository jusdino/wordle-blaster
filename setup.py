#!/usr/bin/env python
import re
from distutils.core import setup

comment = re.compile(r'^\ *#')
with open('requirements.txt', 'r') as f:
    requirements = [x.strip() for x in f if not comment.match(x)]

with open('requirements-bot.txt', 'r') as f:
    bot_requirements = [x.strip() for x in f if not comment.match(x)]

with open('requirements-selenium.txt', 'r') as f:
    selenium_requirements = [x.strip() for x in f if not comment.match(x)]

with open('requirements-dev.txt', 'r') as f:
    dev_requirements = [x.strip() for x in f if not comment.match(x)]

setup(
    name='WordleBlaster',
    version='0.1.0',
    description='Tools for tinkering with Wordle solver algorithms',
    author='Justin Frahm',
    url='https://github.com/jusdino/wordle-blaster',
    packages=['wordle', 'blaster'],
    package_data={'wordle': ['resources/*.txt']},
    install_requires=requirements,
    extras_require={
        'selenium': selenium_requirements,
        'bot': bot_requirements,
        'dev': dev_requirements,
        'all': selenium_requirements + bot_requirements + dev_requirements
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
)
