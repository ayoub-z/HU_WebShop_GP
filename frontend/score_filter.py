import psycopg2
import itertools

# connect to the db
con = psycopg2.connect('host=localhost dbname=huwebshop user=postgres password=Levidov123')

def productfetcher(product_id):
    '''this function fetches all products except the productid in the function arguments'''
    cur = con.cursor()
    cur.execute("SELECT _id, category, selling_price, doelgroep, sub_category, sub_sub_category FROM product WHERE _id != %s", (product_id,))
    return cur.fetchall()

def startproductfetcher(product_id):
    '''this function fetches one specific product'''
    cur = con.cursor()
    cur.execute("SELECT _id, category, selling_price, doelgroep, sub_category, sub_sub_category FROM product WHERE _id = %s", (product_id,))
    return cur.fetchone()

def similarity_score(product_id):
    '''this function assigns similarity score based on category, selling price, doelgroep, sub_cat and sub_sub_cat
    it saves these scores in a dict and returns that dict. Per product, we look at ALL other products and score them'''
    similarity_score_dict = {}
    productlist = productfetcher(product_id)
    startproduct = startproductfetcher(product_id)

    #this allows us to easily adjust the weight of certain attributes. Higher number = higher weight
    categoryweight = 1
    priceweight = 0.5
    doelgroepweight = 2
    sub_categoryweight = 2
    sub_sub_categoryweight = 5

    for product in productlist:
        similarity_score_dict[product[0]] = 0.1
        #category points
        if product[1] == startproduct[1]:
            similarity_score_dict[product[0]] += categoryweight
        if product[2] == 0:
            print('price is 0')
        #price within 20% of start?
        if 120 > (100 * product[2]/startproduct[2]) > 80:
            similarity_score_dict[product[0]] += priceweight
        #doelgroep
        if product[3] == startproduct[3]:
            similarity_score_dict[product[0]] += doelgroepweight
        #sub_sub_category
        if product[4] == startproduct[4]:
            similarity_score_dict[product[0]] += sub_categoryweight
        #sub_sub_category
        if product[5] == startproduct[5]:
            similarity_score_dict[product[0]] += sub_sub_categoryweight
    return similarity_score_dict

def popularity_score():
    '''in this function we assign popularity score to every product.
    since a products popularity is not relative to other products like with similarity, we can run this once
    and then we have every product scored. To score a product, we look at times bought and times viewed
    We give each a weighting and save the total score in a dict which gets returned at the end'''
    cur = con.cursor()
    popularity_score_dict = {}
    cur.execute("SELECT product_id, COUNT(product_id) FROM viewed_before GROUP BY product_id")
    viewcounter = cur.fetchall()
    cur.execute("SELECT product_id, COUNT(product_id) FROM product_order GROUP BY product_id")
    buycounter = cur.fetchall()

    viewweight = 0.01
    buyweight = 0.1

    for i in viewcounter:
        popularity_score_dict[i[0]] = 0.01
        popularity_score_dict[i[0]] += viewweight * i[1]
    for k in buycounter:
        if k[0] in popularity_score_dict.keys():
            #cap buys at 500 to remove bias towards top ~130 products
            if k[1] > 500:
                popularity_score_dict[k[0]] += buyweight * 500
            else:
                popularity_score_dict[k[0]] += buyweight * k[1]
        else:
            popularity_score_dict[k[0]] = 0.01
            popularity_score_dict[k[0]] += buyweight*k[1]

    return popularity_score_dict

def score_combiner(product_id, popdict):
    '''This function combines the scores from similarity_score and popularity_score
    This is also where the calculation happens for the total score.
    It returns the top 4 scoring products in a dictionary.
    We pass this the popularity dict from popularity_score, as not to call that function on loop
    '''

    #get similarity scores for given productid
    productdict = similarity_score(product_id)
    #make new dict to store results
    combine_dict = {}

    #for every product in productdict (all available products are in this dict)
    for i in productdict.items():
        if i[0] in popdict.keys():                     #if we also find this product in popdict
            combine_dict[i[0]] = 0                     # create a new entry in the combination dict
            combine_dict[i[0]] = i[1] * popdict[i[0]]  # multiply the two scores
        else:                                          #if not found in popdict, append the similarity score as total score
            combine_dict[i[0]] = i[1]

    #sort the combined dict based on value, from high to low
    sorted_combine_dict = dict(sorted(combine_dict.items(), key=lambda item: item[1], reverse=True))

    #slice the dict with itertools to only get the top 4 results
    results = dict(itertools.islice(sorted_combine_dict.items(), 4))
    return results

def score_table_maker():
    '''this function creates the table score_recommendation, which has a productid as primary key
    and 4 productids as attributes. It also creates a foreign key constraint for our MAIN productid'''
    cur=con.cursor()
    #making the table and adding foreign key restraint to productid
    cur.execute("CREATE TABLE score_recommendation (productid varchar(255) NOT NULL, product1 varchar(255) NOT NULL, product2 varchar(255) NOT NULL, product3 varchar(255) NOT NULL, product4 varchar(255) NOT NULL, PRIMARY KEY(productid));")
    cur.execute("ALTER TABLE score_recommendation ADD CONSTRAINT FKscore_rec1234 FOREIGN KEY (productid) REFERENCES product (_id);")
    con.commit()

def score_table_filler():
    '''This function should be run after the table score_recommendation has been created,
     with the function score_table_maker.
     This function calls score_combiner to gather the 4 highest scoring products
     It then inserts the original product along with it's 4 highest scoring recommendations into score_recommendation'''
    cur = con.cursor()
    productlist = productfetcher(" ") #run productfetcher with an empty input so we get a list of all products
    popularity_dict = popularity_score()
    # for every product, call score_combiner to find out the best recommendations
    for i in productlist:
        results = [*score_combiner(i[0], popularity_dict)] #using the * operator we can unpack this dict and get the keys from it
        try:
            sqlstatement = "INSERT INTO score_recommendation (productid, product1, product2, product3, product4) VALUES (%s, %s, %s, %s, %s)"
            valuetuple = (i[0], results[0], results[1], results[2], results[3])
            print(f"Inserting {i[0]} with recommendations: {results[0],  results[1], results[2], results[3]}")
            cur.execute(sqlstatement,valuetuple)
            con.commit()
        except Exception as e:
            print(e)
            con.rollback()
    cur.close()

def score_based_filter(productid):
    cur = con.cursor()
    cur.execute("SELECT product1, product2, product3, product4 FROM score_recommendation WHERE productid = %s", (productid,))
    productlist = cur.fetchall()
    prodids = [productlist[0][i] for i in range(0, 4)]
    return prodids