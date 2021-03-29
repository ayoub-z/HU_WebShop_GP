import psycopg2

#connect to the db
con = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=12345')
cur = con.cursor()

def product_combi(lastcartproductid):
	cur.execute("SELECT * FROM product_combination_2 WHERE product_ID = %s", (str(lastcartproductid),))
	productlist = cur.fetchall()
	if productlist[0][5] >= 5:
		prodids = productlist[0][1:5]
		return prodids
	else:
		return None