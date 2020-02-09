# create table crime_data (
# 	id int primary key,
# 	report_date date,
# 	latitude float,
# 	longitude float,
# 	ucr int,
# 	ucr_literal varchar,
# 	crime_harm_index int)
#
# create table homeaway_listings (
# 	id int primary key,
# 	listingId varchar,
# 	price_amt float,
# 	price_avg_nightly float,
# 	price_fees float,
# 	price_rent float,
# 	latitude float,
# 	longitude float,
# 	city varchar,
# 	state varchar,
# 	country varchar,
# 	review_count int,
# 	review_average float,
# 	bathrooms int,
# 	bedrooms int,
# 	listing_url varchar,
# 	book_with_confidence boolean)
#
# create table yelp_data (
#     id int primary key,
#     name varchar,
#     rating float,
#     review_count int,
#     categories varchar,
#     other_id varchar,
#     location varchar,
#     price varchar,
#     latitude float,
#     longitude float)
#
# ALTER TABLE homeaway_listings
#    ADD COLUMN geo_point
#     geometry(Geometry,0);
#
# UPDATE homeaway_listings SET
#   geo_point = ST_Point(longitude, latitude);
#
#
# ALTER TABLE crime_data
#    ADD COLUMN geo_point
#     geometry(Geometry,0);
#
# UPDATE crime_data SET
#   geo_point = ST_Point(longitude, latitude);
#
#
# ALTER TABLE yelp_data
#    ADD COLUMN geo_point
#     geometry(Geometry,0);
#
# UPDATE yelp_data SET
#   geo_point = ST_Point(longitude, latitude);

import psycopg2
engine = psycopg2.connect(
    database="cse6242team22db",
    user="Team22",
    password="vacayaway",
    host="cse6242-db.cvdup1gpakos.us-east-2.rds.amazonaws.com",
    port='5432'
)

cur = engine.cursor()

# cur.execute("SELECT * FROM crime_data limit 10;")
# print(cur.fetchone())
# cur.execute("SELECT * FROM yelp_data limit 10;")
# print(cur.fetchone())
# cur.execute("SELECT * FROM homeaway_listings limit 10;")
# print(cur.fetchone())

cur.execute("select * from homeaway_listings hl join yelp_data yd on st_distance(hl.geo_point::geography, yd.geo_point::geography) < 300 where hl.id = 1;")
print(cur.fetchone())
print(cur.fetchone())

cur.close()
engine.close()