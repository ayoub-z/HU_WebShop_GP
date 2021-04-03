from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import psycopg2
import sys
from product_combi import product_combi_engine
from database_setup.db_connection import cur
from score_filter import score_based_filter
from Category_Reco import *
import json

app = Flask(__name__)
api = Api(app)

class Recom(Resource):
	""" This class represents the REST API that provides the recommendations for
	the webshop. At the moment, the API simply returns a random set of products
	to recommend."""

	def get(self, profileid, count, type='default', productid=None, category=None, sub_category=None, cartproducts=None, lengthcart=0):
		""" This function represents the handler for GET requests coming in
		through the API.
		Specifying type allows us to do different queries depending on the recommendation needed
		Currently only popular product is implemented."""
		#debug print statement, remove from final, sys.stderr prints it to command prompt when executing .sh
		print(f'profileid: {profileid}, count: {count}, type: {type}, category:{category}, sub_category: {sub_category}, lastcartproductid={cartproducts}', file=sys.stderr)
		if type == 'pop_cat':
			return get_matching_prod(category,sub_category), 200
		if type == 'similar':
			return score_based_filter(productid), 200
		if type == 'combination' and lengthcart > 0:
			if product_combi_engine(cartproducts, lengthcart, -1) != None:
				return product_combi_engine(cartproducts, lengthcart, -1), 200
			else:
				pass
		if type == 'popular':
			cur.execute("SELECT productid FROM populairste_prod WHERE rank < 5 ORDER BY random() LIMIT 4")
			productlist = cur.fetchall()
			prodids = [productlist[i][0] for i in range(0, 4)]
			print(f'Type not specified, using DEFAULT', file=sys.stderr)
			return prodids, 200
		else:
			print(f'TYPE NOT IMPLEMENTED, returning empty recommendation', file=sys.stderr)
			return [], 200

# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>/<string:type>/<string:productid>/<string:category>/<string:sub_category>/<string:cartproducts>/<int:lengthcart>/")