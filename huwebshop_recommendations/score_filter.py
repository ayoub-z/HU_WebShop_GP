def score_based_filter(productid, cur):
    '''this is the final function that fetches the finished entries from the SQL database'''
    cur.execute("SELECT product1, product2, product3, product4 FROM score_recommendation WHERE productid = %s", (productid,))
    productlist = cur.fetchall()
    prodids = [productlist[0][i] for i in range(0, 4)]
    return prodids
