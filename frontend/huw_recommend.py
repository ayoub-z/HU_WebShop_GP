from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import psycopg2
import sys

app = Flask(__name__)
api = Api(app)

#connect to the db
con = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=Levidov123')
cur = con.cursor()

class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def get(self, profileid, count, type='default'):
        """ This function represents the handler for GET requests coming in
        through the API.
        Specifying type allows us to do different queries depending on the recommendation needed
        Currently only popular product is implemented."""

        if type == 'popular':
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
        else:
            cur.execute("SELECT productid FROM populairste_prod WHERE rank < 5 ORDER BY random() LIMIT 4")
            productlist = cur.fetchall()
            prodids = [productlist[i][0] for i in range(0, 4)]
            print(f'TYPE NOT IMPLEMENTED, returning productids: {prodids}', file=sys.stderr)
            return prodids, 200

# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>/<string:type>/")