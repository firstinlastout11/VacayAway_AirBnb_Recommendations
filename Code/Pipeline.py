######################################### 0 - Imports ################################################################
import pandas as pd
import numpy as np
from utils_general import start_SQL_engine
from utils_homeaway import scrape_data
from utils_scoring import score_noSA as score_data
from utils_distanceScore import calculate_DS as add_yelp_data
from utils_crimeScore import add_crime_score_mod as add_crime_score
from utils_SQL import update_homeaway_tbl
import time


######################################### 0 - Preliminaries ###########################################################

bool_verbose = False
bool_save = False # save the scraped HomeAway data to a CSV
bool_test = False

if(bool_verbose):
    print("########## STARTING SQL ENGINE ##########")


engine = start_SQL_engine()

######################################### 1 - Read in data from Tableau ###############################################

# dummy values - DEBUG
# these dummy values are the formatted output values from Tableau
search_string = "Atlanta, GA"
date_start = "2019-07-01"
date_end = "2019-07-09"
user_weights = pd.DataFrame(index = [0],
                      data = {
                          'price_rent': 5,
                          'review_average': 5,
                          'crime_score': 5,
                          'UC1-DS': 3,
                          'UC2-DS': 5,
                          'UC3-DS': 2
                      })

# define test UC pairs of Primary/Secondary Categories

cat1 = 'Food'
subcat1 = 'Poke'

cat2 = 'Active Life'
subcat2 = 'Golf'

cat3 = 'Night Life'
subcat3 = 'Bars'

######################################### 2 - Scrape listings from HomeAway API ########################################



if(bool_verbose):
    print("########## IMPORTING DATA ##########")

if(bool_test):
    data_1 = pd.read_csv('homeaway_data.csv').drop(['Unnamed: 0'], axis=1)
else:
    #start = time.time()
    data_1 = scrape_data(search_string, date_start, date_end, bool_save, bool_verbose)
    #print("completed in ",time.time()-start, "seconds")

# Update SQL table `homeaway_v2` with data_2

if(bool_verbose):
    print("########## APPENDING TO SQL TABLE -HOMEAWAY_V2- ##########")

update_homeaway_tbl(engine, data_1, bool_verbose)


######################################### 3 - Complete Feature Vector #################################################


########### A - append Crime scores to listings ###########

if(bool_verbose):
    print("########## CALCULATING CRIME SCORE ##########")

data_2 = add_crime_score(data_1, engine)

# # Update SQL table `homeaway_v2` with data_2

if(bool_verbose):
    print("########## APPENDING TO SQL TABLE -HOMEAWAY_V2- ##########")

update_homeaway_tbl(engine, data_2, bool_verbose)


########### B - append Yelp scores to listings ###########

if(bool_verbose):
    print("########## CALCULATING YELP DISTANCE SCORES ##########")

data_3 = add_yelp_data(cat1, subcat1, cat2, subcat2, cat3, subcat3, engine)


######################################### 4 - Score Listings ##########################################################

if(bool_verbose):
    print("########## RANKING LISTINGS ##########")

data_4 = score_data(data_3, user_weights, bool_verbose)

# Output is `data_4`

data_4 = data_4.dropna()

if(bool_verbose):
    print("########## EXECUTION COMPLETE ##########")

######################################### 5 - Output to Tableau #######################################################