import psycopg2
from database_setup.db_connection import cur
import sys

def product_combi(lastcartproductid):
	'''
	Function returns the best 4 products that combine with the given product_id from shopping cart 
	'''

	# sql query retrieves all 4 products that are a good combination with this product_id from table "product_combination"
	cur.execute("SELECT * FROM product_combination WHERE product_ID = %s", (str(lastcartproductid),))
	productlist = cur.fetchall()
	print(productlist, file=sys.stderr)
	# checks that the count of how often the last product is bought is at least 5 or higher
	try:
		if productlist[0][5] >= 5:
			prodids = productlist[0][1:5]
			return prodids
	except Exception as e:
		print(e, file=sys.stderr)
		return None