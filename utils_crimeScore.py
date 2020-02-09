import pandas as pd
import psycopg2

def get_crime_score(t_lat, t_long, engine):    
    cur = engine.cursor()
    
    str_cmd_block_1 = """SELECT crime_score FROM neighborhoods nb JOIN T nbc ON nbc.gid = nb.gid WHERE st_contains(nb.atl_geom, st_setsrid(st_point"""
    
    str_cmd_block_2 = str((t_long, t_lat))

    str_cmd_block_3 = """, 4326))"""

    str_cmd = str_cmd_block_1 + str_cmd_block_2 + str_cmd_block_3

    #print(str_cmd)

    cur.execute(str_cmd)
    response = cur.fetchall()
    if(len(response) == 0): # if there's no value returned
        crime_score = 513
    else:
        df_cs = pd.DataFrame(response, columns=[desc[0] for desc in cur.description])
        crime_score = df_cs.crime_score[0]
        #crime_score = response[0][0]
    #print(response)
    return(crime_score)

def add_crime_score(df_homeaway, engine):
    df_homeaway['crime_score'] = 0 # instantiate column
    #print(df_homeaway.shape[0])
    for i in range(df_homeaway.shape[0]):
        #print(i)
        df_homeaway['crime_score'][i] = get_crime_score(df_homeaway['latitude'][i], df_homeaway['longitude'][i], engine)
    return(df_homeaway)


def add_crime_score_mod(df_homeaway, engine): # this method depends on having the `geo_point` field already filled
    cur = engine.cursor()
    str_cmd = """
    SELECT *
    FROM (
        SELECT listing_id, gid 
        FROM homeaway_v2
        JOIN neighborhoods nb ON st_contains(nb.atl_geom, st_setsrid(geo_point, 4326))
        ) A
    JOIN T ON A.gid = T.gid
    """
    cur.execute(str_cmd)
    response = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
    df_homeaway['crime_score'] = response['crime_score']
    return(df_homeaway)