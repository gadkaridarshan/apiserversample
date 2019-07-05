# ===================================
# This controller class uses the
# Coordinates Model and the Stores models
# to build data for the view/templates
# Author        : Darshan Gadkari
# Created       : Jun 2019
# ===================================
from geopy.distance import geodesic
import pandas as pd

from helpers.PostcodeHelper import PostcodeHelper


class Controller:
    def __init__(self, store_model, coordinate_model):
        """
        Constructor
        Creates instances of Store and Coordinate models.
        Parameters
        ----------
        store_model: model.Stores
            Receives the Stores model object
        coordinate_model: model.Coordinates
            Receives the Coordinates model object
        """
        self.store_model = store_model
        self.coordinate_model = coordinate_model

    def get_distance_between_coords(self, coord1, coord2, distance_in='km'):
        """
        Given two dictionaries that have a latitude element
        and a longitude element, return the distance between
        those two coordinates.
        Parameters
        ----------
        coord1: dict
            Coordinate 1 to calculate the distance from
        coord1: dict
            Coordinate 2 to calculate the distance to

        Returns
        -------
        float
            Distance between the coordinates
        """
        point1 = (coord1['latitude'], coord1['longitude'])
        point2 = (coord2['latitude'], coord2['longitude'])
        return getattr(geodesic(point1, point2), distance_in)

    def merge_dict_lists(self, dicts_1, dicts_2, key='postcode'):
        """
        A function to join two dictionary lists on a specified key.
        We will use pandas dataframe to do that join - pandas
        DataFrame use vector processing and will be much faster
        than core Python
        Parameters
        ----------
        dicts_1: list
            list of dictionaries that contain the following keys:
                name
                postcode
        dicts_1: list
            list of dictionaries that contain the following keys:
                latitude
                longitude
                postcode

        Returns
        -------
        list
            list of dictionaries that contain the following keys:
                latitude
                longitude
                postcode
                name
        """
        df_1 = pd.DataFrame.from_dict(dicts_1)
        # ensure that postcodes are all in upper case
        df_1['postcode'] = df_1[key].str.upper()
        df_2 = pd.DataFrame.from_dict(dicts_2)
        # ensure that postcodes are all in upper case
        df_2['postcode'] = df_2[key].str.upper()

        # They need to be the same length - that is why we will
        # use inner join
        return df_1.merge(
                            df_2,
                            on=[key],
                            how='inner'
                        ).to_dict(orient='records')

    def get_coordinates(self, postcodes):
        """
        Obtains the API response from the model and builds the postcode
        coordinate objects through the postcode factory
        Parameters
        ----------
        postcodes: list
            A list of postcodes to ask the API for

        Returns
        -------
        list
            A list of cleaned up postcodes
        """
        return [
            PostcodeHelper.build_dict(api_response=api_response)
            for api_response
            in self.coordinate_model.get_coordinates(postcodes)]

    def get_long_lat_of_store(self):
        """
        Pulls the postcodes from the store and calculates the longitude and
        latitude for each postcode. Returns a list
        of dictionaries
        Returns
        -------
        list
            A list of postcodes
        """
        store_data = self.store_model.get_store_data()
        postcodes = pd.DataFrame(store_data)['postcode'].tolist()
        postcode_coord = self.get_coordinates(postcodes)

        # The API doesn't ALWAYS return the names that match the store.
        # So join these two data sets
        return self.merge_dict_lists(postcode_coord, store_data, 'postcode')

    def get_postcodes_in_radius(self, postcode, radius=0, distance_in='km'):
        """
        Return a list of postcodes that lie within a
        specified radius as well as the measurement of distance
        Parameters
        ----------
        postcode: str
            UK format post code
        radius: int
            radius to search other postcodes
        distance_in: str
            distance type, example: 'mi', 'km'
            default: 'km'

        Returns
        -------
        list
            A list of postcodes
        """

        inside_radius = []
        all_postcodes = self.get_long_lat_of_store()

        # since Coordinate Model's get_coordinates() returns a list
        # we take the first element in the list
        lkp = PostcodeHelper.build_dict(
            api_response=self.coordinate_model.get_coordinates(postcode)[0])

        # We cannot find distance for a postcode with no coordinates
        # from the API
        if lkp['latitude'] == 'NONE FOUND' or lkp['latitude'] == 'NONE FOUND':
            return []

        for ele in all_postcodes:
            if ele['postcode'] == postcode:
                # Skip the supplied postcode.
                continue
            elif 'NONE FOUND' in ele.values():
                # Skip codes with no coordinates
                continue

            distance = self.get_distance_between_coords(
                lkp,
                ele,
                distance_in=distance_in)

            if distance <= radius:
                inside_radius.append(ele['postcode'])

        return inside_radius
