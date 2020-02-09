import psycopg2


def start_SQL_engine(): #connect to the PostGre SQL database on AWS
    engine = psycopg2.connect(
        database="cse6242team22db",
        user="Team22",
        password="vacayaway",
        host="cse6242-db.cvdup1gpakos.us-east-2.rds.amazonaws.com",
        port='5432'
    )
    return(engine)