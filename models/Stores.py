# ===================================
# StoreModel: Load the store.json file from the static
# files folder and cache the load in an instance
# of the class to not reload the file on every request
# with the postcode API
# Author        : Darshan Gadkari
# Created       : Jun 2019
# ===================================

import json
import os
import pandas as pd


class StoreModel:
    def __init__(self):
        """
        Constructor
        Read the json file that represents
        store data
        """
        stores_json_path = os.path.dirname(os.path.abspath(__file__)) + \
            '/../static/stores.json'
        self.stores = json.load(open(stores_json_path))

    def get_store_data(self):
        """
        Return a list of stores (dicts)
        sorted alphabetically by the store names
        Returns
        -------
        list
            A list of postcodes as dictionaries
        """
        return pd.DataFrame(self.stores).sort_values(['name']).\
            to_dict(orient='records')
