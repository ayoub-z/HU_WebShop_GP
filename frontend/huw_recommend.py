from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import psycopg2
import sys
from product_combi import product_combi
from database_setup import db_connection
from score_filter import score_based_filter
from category_reco import *

app = Flask(__name__)
api = Api(app)

class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def get(self, profileid, count, type='default', productid=None, category=None, sub_category=None, lastcartproductid=None):
        """ This function represents the handler for GET requests coming in
        through the API.
        Specifying type allows us to do different queries depending on the recommendation needed
        Currently only popular product is implemented."""
        #debug print statement, remove from final, sys.stderr prints it to command prompt when executing .sh
        print(f'profileid: {profileid}, count: {count}, type: {type}, category:{category}, sub_category: {sub_category}, lastcartproductid={lastcartproductid}', file=sys.stderr)
        if type == 'pop_cat':
            return get_matching_prod(category,sub_category), 200
        if type == 'similar':
            return score_based_filter(productid, db_connection.cur), 200
        if type == 'combination':
            # returns 4 products from the database that are a good combination with the given product_id
            if product_combi(lastcartproductid) == None:
                pass
            else:
                return product_combi(lastcartproductid), 200
        else:
            print(f'TYPE NOT IMPLEMENTED, returning empty recommendation', file=sys.stderr)
            return [], 200

# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>/<string:type>/<string:productid>/<string:category>/<string:sub_category>/<string:lastcartproductid>/")