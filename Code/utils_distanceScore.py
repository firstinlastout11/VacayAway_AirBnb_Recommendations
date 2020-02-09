import numpy as np
import pandas as pd
import sys
import psycopg2


def calculate_UC_DS(str_category, str_subcategory, engine):
    cur = engine.cursor()

    #str_category = 'Food'
    #str_subcategory = 'Poke'

    # Construct SQL command

    str_cmd_block1 = """
    SELECT rank_filter.* FROM (
        SELECT hl.index,
            hl.listing_id,
            hl.review_average,
            hl.price_rent,
            hl.bathrooms,
            yd.name,
            yd.rating,
            yd.primary_categories,
            yd.secondary_categories,
            yd.price,
            yd.categories,
            hl.crime_score,
            st_distance(hl.geo_point::geography, yd.geo_point::geography) as distance,
            rank() OVER (
                PARTITION BY hl.index
                ORDER BY st_distance(hl.geo_point::geography, yd.geo_point::geography)
                )
            FROM yelp_data yd, homeaway_v2 hl
            WHERE primary_categories Like CONCAT('%',"""

    str_cmd_block2 = '\'' + str_category + '\''

    str_cmd_block3 = """,'%') and secondary_categories Like CONCAT('%', """

    str_cmd_block4 = '\'' + str_subcategory + '\''

    str_cmd_block5 = """, '%') and yd.rating > 2.5
    ) rank_filter WHERE RANK <= 5;"""

    str_cmd = str_cmd_block1 + str_cmd_block2 + str_cmd_block3 + str_cmd_block4 + str_cmd_block5

    # execute SQL command and recieve output

    cur.execute(str_cmd)
    response = cur.fetchall()
    temp_df = pd.DataFrame(response)

    # Rename columns for readability
    temp_df = temp_df.rename(index=str, columns={
        0: "id",
        1: "listingId",
        2: "review_average",
        3: "price_rent",
        4: "bathrooms",
        5: "yd_name",
        6: "yd_rating",
        7: "yd_primary_categories",
        8: "yd_secondary_categories",
        9: "yd_price",
        10: "yd_categories",
        11: "crime_score",
        12: "distance",
        13: "rank"
    })

    temp_df.loc[temp_df['distance'] == 0, 'distance'] = 0.01

    temp_df['D'] = temp_df['rank'] / temp_df['distance']

    temp_df_agg = temp_df.groupby('id').agg({
        'listingId': 'first',
        'review_average': 'first',
        'price_rent': 'first',
        'bathrooms': 'first',
        'yd_rating': 'first',
        'crime_score': 'first',
        'D': 'sum'
    })

    output_score = temp_df_agg['D']

    return(output_score)



def calculate_DS(cat1, subcat1, cat2, subcat2, cat3, subcat3, engine):
	# Step 1: Obtain the LC-CS
	cur_LC_CS = engine.cursor()

	str_cmd_LC_CS = """SELECT index,listing_id,review_average,price_rent, bathrooms, crime_score
	FROM homeaway_v2
	ORDER BY index"""

	cur_LC_CS.execute(str_cmd_LC_CS)

	response_LC_CS = cur_LC_CS.fetchall()
	df_LC_CS = pd.DataFrame(response_LC_CS)

	# Rename columns for readability
	df_LC_CS = df_LC_CS.rename(index=str, columns={
	    0: "id",
	    1: "listingId",
	    2: "review_average",
	    3: "price_rent",
	    4: "bathrooms",
	    5: "crime_score",
	})

	df_LC_CS['UC1-DS'] = list(calculate_UC_DS(cat1, subcat1, engine))
	df_LC_CS['UC2-DS'] = list(calculate_UC_DS(cat2, subcat2, engine))
	df_LC_CS['UC3-DS'] = list(calculate_UC_DS(cat3, subcat3, engine))

	return(df_LC_CS)