# ===================================
# Create the Stores Blueprint object that
# define the routes
# to build data for the view/templates
# Author        : Darshan Gadkari
# Created       : Jun 2019
# ===================================
from flask import Blueprint, render_template, jsonify, request
from controllers.Controller import Controller

from models.Coordinates import CoordinatesModel
from models.Stores import StoreModel

blueprint = Blueprint(
    'stores_blueprint',
    __name__,
    template_folder='../templates')

# Create all our models to pass to their controllers.
store_model = StoreModel()
coordinates_model = CoordinatesModel()

# Create all the controllers we need. Pass them the requires models.
controller = Controller(
    store_model=store_model,
    coordinate_model=coordinates_model)


# this endpoint returns json rendered as html
@blueprint.route('/')
def render_stores_page():
    page_data = get_data()
    return render_template('stores.html', store_list=page_data)

# this endpoint returns raw json of all the postcodes
@blueprint.route('/data')
def render_data():
    return jsonify(get_data())


# this function gets the data that can be used by the above
# functions
def get_data():
    return controller.get_long_lat_of_store()

# this endpoint returns raw json of the postcodes
# within a specified radius
@blueprint.route('/radius', methods=['POST'])
def get_by_radius():
    content = request.json
    postcode = content['postcode'] if 'postcode' in content else 'AL9 5JP'
    radius = content['radius'] if 'radius' in content else 20
    distance_in = content['distance_in'] if 'distance_in' in content else 'km'
    return jsonify(controller.get_postcodes_in_radius(
        postcode=postcode,
        radius=radius,
        distance_in=distance_in))
