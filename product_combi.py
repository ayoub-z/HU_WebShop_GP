import psycopg2

#connect to the db
con = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=12345')
cur = con.cursor()

def product_combi(lastcartproductid):
	'''
	Function returns the best 4 products that combine with the given product_id from shopping cart 
	'''

	# sql query retrieves all 4 products that are a good combination with this product_id from table "product_combination"
	cur.execute("SELECT * FROM product_combination WHERE product_ID = %s", (str(lastcartproductid),))
	productlist = cur.fetchall()
	# checks that the count of how often the last product is bought is at least 5 or higher
	if productlist[0][5] >= 5:
		prodids = productlist[0][1:5]
		return prodids
	else:
		return None