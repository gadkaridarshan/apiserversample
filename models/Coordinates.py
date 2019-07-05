# ===================================
# CoordinatesModel: Model class to interact
# with the postcode API
# Author        : Darshan Gadkari
# Created       : Jun 2019
# ===================================

import requests
from os import getenv
from dotenv import load_dotenv
from helpers.LogHelper import LogHelper
from helpers.Logging import LOGGER

logger = LOGGER(name=__name__).get_logger()


class CoordinatesModel:
    def __init__(self):
        """
        Constructor
        Reads the env file and gets the
        api URL
        """
        load_dotenv('settings/.env')
        self.api_url = getenv('POSTCODE_API')

    def get_coordinates(self, postcodes, chunk_size=200):
        """
        Takes in a list of postcodes or a single postcode
        and will return a list of dictionaries
        Parameters
        ----------
        postcodes: list
            A list of postcodes
        chunk_size: int
            since we call an external API, it is better to chunk it
            default: 200

        Returns
        -------
        list
            A list of postcodes as dictionaries
        """
        if type(postcodes) is not list:
            # Allow a single postcode or a list of postcodes.
            postcodes = [postcodes]
        api_result = []

        # generator object of chunks to iterate over
        chunks = (
            postcodes[i:i + chunk_size]
            for i in range(0, len(postcodes), chunk_size))
        for chunk in chunks:
            try:
                res = requests.post(
                    self.api_url,
                    headers={
                                'Content-type': 'application/json',
                                'Accept': 'text/plain'
                            },
                    json={'postcodes': chunk}
                    )
                logger.info('Request made successfully')
                logger.info('chunk_size: {chunk_size}'.format(
                    chunk_size=chunk_size))
            except requests.exceptions.HTTPError as e:
                LogHelper.requests_error_log(
                    error_message='HTTP error connecting to {}.'.
                    format(self.api_url),
                    e=e)
            except requests.exceptions.Timeout as e:
                LogHelper.requests_error_log(
                    error_message='Timed out connecting to {}.'.
                    format(self.api_url),
                    e=e)
            except requests.exceptions.TooManyRedirects as e:
                LogHelper.requests_error_log(
                    error_message='Bad URL {}. Please check it.'.
                    format(self.api_url),
                    e=e)
            except requests.exceptions.ConnectionError as e:
                LogHelper.requests_error_log(
                    error_message='Cannot connect to {}.'.
                    format(self.api_url),
                    e=e)
            except requests.exceptions.RequestException as e:
                LogHelper.requests_error_log(
                    error_message='Some other error connect to {}.'.
                    format(self.api_url),
                    e=e)

            res = res.json()['result']
            api_result.extend(res)

        return api_result
