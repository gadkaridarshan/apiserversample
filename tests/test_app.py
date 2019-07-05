# ===================================
# Unit test using unittest package
# Author        : Darshan Gadkari
# Created       : Jun 2019
# ===================================
import unittest
from json import loads, dumps

from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_app(self):
        """
        Test the main app
        """
        rv = self.app.get('/')
        assert rv.status == '200 OK'

    def test_route_main(self):
        """
        Test the main route
        """
        rv = self.app.get('/')
        assert b'Solution to the Code Challenge' in rv.data

    def test_route_data(self):
        """
        Test the data route
        """
        rv = self.app.get('/data')
        data = loads(rv.data)
        assert isinstance(data, list)
        self.assertEqual(len(data), 95)
        for item in data:
            assert isinstance(item, dict)
            assert 'latitude' in item.keys()
            assert 'longitude' in item.keys()
            assert 'name' in item.keys()
            assert 'postcode' in item.keys()
            assert len(item['postcode']) > 5

    def test_route_radius_km_1(self):
        """
        First Test the radius route with distance in kilometers
        """
        post_data = {
                        'postcode': 'N11 3PW',
                        'radius': 10,
                        'distance_in': 'km'
                    }
        headers = {'Content-type': 'application/json'}
        rv = self.app.post('/radius', data=dumps(post_data), headers=headers)
        data = loads(rv.data)
        assert isinstance(data, list)
        self.assertEqual(len(data), 4)
        for item in data:
            assert isinstance(item, str)
            assert len(item) > 5

    def test_route_radius_km_2(self):
        """
        Second Test the radius route with distance in kilometers
        """
        post_data = {
                        'postcode': 'EN1 1TH',
                        'radius': 10,
                        'distance_in': 'km'
                    }
        headers = {'Content-type': 'application/json'}
        rv = self.app.post('/radius', data=dumps(post_data), headers=headers)
        data = loads(rv.data)
        assert isinstance(data, list)
        self.assertEqual(len(data), 3)
        for item in data:
            assert isinstance(item, str)
            assert len(item) > 5

    def test_route_radius_mi_1(self):
        """
        First Test the radius route with distance in miles
        """
        post_data = {
                        'postcode': 'N11 3PW',
                        'radius': 10,
                        'distance_in': 'mi'
                    }
        headers = {'Content-type': 'application/json'}
        rv = self.app.post('/radius', data=dumps(post_data), headers=headers)
        data = loads(rv.data)
        assert isinstance(data, list)
        self.assertEqual(len(data), 9)
        for item in data:
            assert isinstance(item, str)
            assert len(item) > 5

    def test_route_radius_mi_2(self):
        """
        Second Test the radius route with distance in miles
        """
        post_data = {
                        'postcode': 'EN1 1TH',
                        'radius': 10,
                        'distance_in': 'mi'
                    }
        headers = {'Content-type': 'application/json'}
        rv = self.app.post('/radius', data=dumps(post_data), headers=headers)
        data = loads(rv.data)
        assert isinstance(data, list)
        self.assertEqual(len(data), 8)
        for item in data:
            assert isinstance(item, str)
            assert len(item) > 5
