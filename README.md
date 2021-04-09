# HU_WebShop_GP
Levi Verhoef, Ayoub Zouin, Dennis Besselsen

This is our recommendation engine project.

We have implemented a few algorithms to make recommendations. To be able to view this, you will need to have the database setup as supplied by the HU.
Then in order to run this, make sure you open database_setup/db_connection.py and change the database variables.
There's 2 database tables that need to be filled beforehand. To do this, run score_based_recommendation_table_setup and product_combi_filler.
Now, run huw.sh and huw_recommend.sh, and navigate to 127.0.0.1:5000.
There you will see the frontend, and you can check the recommendations.

Currently we're implementing 3 different recommendations and 1 default recommendation on the webpages: 
1. On the homepage you will find the default recommendation ("**Simple algorithm**").
2. On the category page we have implemented the **Category based popularity recommendation** recommendation.
3. On the product page we have implemented the **Score-based filter vergelijkbare producten** recommendation.
4. Finally, on the shopping cart page we have implemented the **Product Combination** recommendation.
