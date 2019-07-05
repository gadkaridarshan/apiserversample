# ===================================
# helper module for logging purposes
# Author        : Darshan Gadkari
# Created       : Jun 2019
# ===================================

import logging
from logging.handlers import RotatingFileHandler


class LOGGER:
    def __init__(self, name='App'):
        """
        Constructor
        Parameters
        ----------
        name: str
            Name for the Logging object
            default: 'App'
        """
        FORMAT = '%({v})-6s%({a})-15s %({f})-20s %({n})-25s %({i})-6s%({m})s'.\
            format(
                v='levelname',
                a='asctime',
                f='filename',
                n='funcName',
                i='lineno',
                m='message')
        logging.basicConfig(
            level=logging.DEBUG,
            format=FORMAT,
            handlers=[RotatingFileHandler(
                'logs/app.log',
                maxBytes=10000000,
                backupCount=10)])
        self.LOGGER = logging.getLogger(name=name)
        self.LOGGER.setLevel(logging.INFO)

    def get_logger(self):
        """
        Returns the logger object
        Returns
        -------
        LOGGER object
            LOGGER object that can be used for logging
        """
        return self.LOGGER
