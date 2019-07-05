# ===================================
# Postcode Helper module
# Author        : Darshan Gadkari
# Created       : Jun 2019
# ===================================


class PostcodeHelper:
    @classmethod
    def build_dict(cls, api_response):
        """
        Accepts the API response and returns a dict
        with only the keys/values that are required
        Parameters
        ----------
        api_response: dict
            The complete api response that has to be parsed

        Returns
        -------
        dict
            A compact dict with only the required keys/values
        """
        if api_response['result']:
            return {
                'postcode': api_response['query'],
                'latitude': api_response['result']['latitude'],
                'longitude': api_response['result']['longitude']
            }
        else:
            return {
                'postcode': api_response['query'],
                'longitude': 'NONE FOUND',
                'latitude': 'NONE FOUND'
            }
