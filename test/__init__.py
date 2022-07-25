import os
import logging

logging.basicConfig(
    format='%(asctime)s %(module)s-%(funcName)s: %(levelname)-8s %(message)s',
    filename='test.log',
    filemode='w',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
if os.environ.get('DEBUG', '').lower() == 'true':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
