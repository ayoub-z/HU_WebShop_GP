from flask import Flask
from flask_restful import Api, Resource
import psycopg2
import sys
from score_filter import score_based_filter
from product_combi import product_combi
from database_setup.db_connection import cur

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
            cur.execute("SELECT productid FROM populairste_prod WHERE rank < 200 ORDER BY random() LIMIT 4")
            productlist = cur.fetchall()
            prodids = [productlist[i][0] for i in range(0, 4)]
            return prodids, 200
        if type == 'default':
            cur.execute("SELECT productid FROM populairste_prod WHERE rank < 5 ORDER BY random() LIMIT 4")
            productlist = cur.fetchall()
            prodids = [productlist[i][0] for i in range(0, 4)]
            print(f'Type not specified, using DEFAULT', file=sys.stderr)
            return prodids, 200
        if type == 'similar':
            return score_based_filter(productid), 200
        if type == 'combination':
            # returns 4 products from the database that are a good combination with the given product_id
            return product_combi(lastcartproductid), 200
        else:
            cur.execute("SELECT productid FROM populairste_prod WHERE rank < 5 ORDER BY random() LIMIT 4")
            productlist = cur.fetchall()
            prodids = [productlist[i][0] for i in range(0, 4)]
            print(f'TYPE NOT IMPLEMENTED, returning productids: {prodids}', file=sys.stderr)
            return prodids, 200

# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>/<string:type>/<string:productid>/<string:category>/<string:sub_category>/<string:lastcartproductid>/")