# ===================================
# Log Helper class
# Author        : Darshan Gadkari
# Created       : Jun 2019
# ===================================
from helpers.Logging import LOGGER

logger = LOGGER(name=__name__).get_logger()


class LogHelper:
    @classmethod
    def requests_error_log(self, error_message, e):
        """
        Takes error message and error stack and
        writes it to log
        Parameters
        ----------
        error_message: str
            Error message
        e: str
            Error stack

        Raises
        ------
        e: str
            Error stack that is passed as parameter

        Returns
        -------
        None
        """
        logger.error('HTTP error connecting to {}.'.format(self.api_url))
        logger.error('Error: {e}'.format(e=e))
        raise e
