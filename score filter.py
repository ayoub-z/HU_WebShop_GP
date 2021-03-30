import psycopg2
import itertools

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

def popularity_score():
    cur = con.cursor()
    popularity_score_dict = {}
    cur.execute("SELECT product_id, COUNT(product_id) FROM viewed_before GROUP BY product_id")
    viewcounter = cur.fetchall()
    cur.execute("SELECT product_id, COUNT(product_id) FROM product_order GROUP BY product_id")
    buycounter = cur.fetchall()

    for i in viewcounter:
        popularity_score_dict[i[0]] = 0.01
        popularity_score_dict[i[0]] += 0.01 * i[1]
    for k in buycounter:
        if k[0] in popularity_score_dict.keys():
            popularity_score_dict[k[0]] += 0.05 * k[1]
        else:
            popularity_score_dict[k[0]] = 0.01
            popularity_score_dict[k[0]] += 0.05*k[1]
    return popularity_score_dict

def score_combiner(product_id):
    #get popularity scores
    popdict = popularity_score()
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
    print(results)
    #add SQL insert here

score_combiner("45281")
