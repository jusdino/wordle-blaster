# WordleBlaster
This project is more a framework to enable tinkering on different algorithms to solve Wordles than it is any especially clever algorithms themselves.

This project includes a python api wrapper around the real Wordle browser app via a [Selenium driver](https://selenium-python.readthedocs.io/) as well as a SimWordle version that implements the same api as a python simulation for much faster and convenient testing.

## Installation
This is a python 3.8+ project. To install any dependencies you can use python's package manager, `pip`.
- Clone this repository to your computer (`git clone https://github.com/jusdino/wordle-blaster.git`)
- The package is divided into it's basic requirements and optional extras listed in the subsequent steps. Run `pip install .` for just the basics.
- If you want to use the `Wordle` class to run a Blaster against a real Wordle, you will need to install the [geckodriver](https://github.com/mozilla/geckodriver/releases) and install the `selenium` extra dependencies (`pip install .[selenium]`)
- If you want to use the included bot script to post as a bot to discord/slack, install the `bot` extra dependencies (`pip install .[bot]`)
- If you want to go whole-hog, just install everything and be done, run `pip install .[all]`. Note that the above geckodriver install is still a required extra step.

## Packages
### [wordle](./wordle/)
This package includes the Wordle class, a selenium-based python api that wraps the browser app and the SimWordle class, which is pure-python and implements the same api, more suitable for testing.

### [blaster](./blaster/)
This package includes the `BasicWordleBlaster` class, which is my attempt at implementing the tedious bits of reading the results of a submitted guess and tracking constraints on the possible solution, based on the evaluation returned by Wordle. This class is assuming a 'hard-mode' like behavior (in 'hard-mode', you _must_ guess only possible solution words, using what you know) but allows a developer to easily extend the method used to choose from candidate solution words. The BasicWordleBlaster behavior is to just pick a random candidate word based on the constraints established so far, rather than do anything intelligent strategically.
