#!/usr/bin/python3
import logging
from Red_lib.config import CONF
#from config import CONF

logger = logging.getLogger(CONF.LOG.app_name)
logger.setLevel(CONF.LOG.root_level)

fh = logging.FileHandler(CONF.LOG.logfilename)
fh.setLevel(CONF.LOG.fh_level)
ch = logging.StreamHandler()
ch.setLevel(CONF.LOG.ch_level)
formatter = logging.Formatter(CONF.LOG.log_format)

ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

'''
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
'''
