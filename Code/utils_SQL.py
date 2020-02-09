import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def update_homeaway_tbl(engine, df_homeaway_v2, bool_verbose):
    pd_engine = create_engine('postgresql://Team22:vacayaway@cse6242-db.cvdup1gpakos.us-east-2.rds.amazonaws.com:5432/cse6242team22db')
    cur = engine.cursor()
    if(bool_verbose):
    	print("|-------DROPPING TABLE -homeaway_v2-")
    cur.execute("""DROP TABLE if exists homeaway_v2;""")
    engine.commit()
    if(bool_verbose):
    	print("|-------CREATING UPDATED TABLE -homeaway_v2-")
    df_homeaway_v2.to_sql('homeaway_v2', pd_engine)
    cur.execute("""ALTER TABLE homeaway_v2 ADD COLUMN geo_point geometry(Geometry,0);""")
    cur.execute("""UPDATE homeaway_v2 SET geo_point = ST_POINT(longitude, latitude);""")
    engine.commit()