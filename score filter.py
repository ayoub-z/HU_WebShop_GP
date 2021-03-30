import psycopg2

# connect to the db
con = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=Levidov123')

def productfetcher(product_id):
    cur = con.cursor()
    cur.execute("SELECT _id, category, selling_price, doelgroep, sub_category, sub_sub_category FROM product WHERE _id != %s", (product_id,))
    return cur.fetchall()

def startproductfetcher(product_id):
    cur = con.cursor()
    cur.execute("SELECT _id, category, selling_price, doelgroep, sub_category, sub_sub_category FROM product WHERE _id = %s", (product_id,))
    return cur.fetchone()

def similarity_score(product_id):
    similarity_score_dict = {}
    productlist = productfetcher(product_id)
    startproduct = startproductfetcher(product_id)

    for product in productlist:
        similarity_score_dict[product[0]] = 0.1
        #category points
        if product[1] == startproduct[1]:
            similarity_score_dict[product[0]] += 1
        if product[2] == 0:
            print('price is 0')
        #price within 20% of start?
        if 120 > (100 * product[2]/startproduct[2]) > 80:
            similarity_score_dict[product[0]] += 0.4
        #sub_category
        if product[3] == startproduct[3]:
            similarity_score_dict[product[0]] += 1
        #sub_category
        if product[4] == startproduct[4]:
            similarity_score_dict[product[0]] += 2
    return similarity_score_dict

def popularity_score(product_id):
    cur = con.cursor()
    popularity_score_dict = {}
    cur.execute("SELECT product_id, COUNT(product_id) FROM viewed_before GROUP BY product_id")
    viewcounter = cur.fetchall()

    for i in viewcounter:
        popularity_score_dict[i[0]] = 0.01
        popularity_score_dict[i[0]] += 0.01 * i[1]
    print(popularity_score_dict)




popularity_score("45281")
