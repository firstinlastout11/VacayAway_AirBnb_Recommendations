DESCRIPTION
        This project is designed to give people going on vacation a better way to find rental home recommendations. It utilizes Tableau for the visualization, python for the back-end and PostgreSQL to store the data. You will need access to Tableau in order to view this project. 


REQUIREMENTS
1. Postgres 11.0
2. Tableau Desktop 2019.1.2
3. Python 3.x



INSTALLATION
1. Postgres Setup:
   1. Set up a Postgres 11 database and import the attached database to set up seed data.
https://gtvault-my.sharepoint.com/:u:/g/personal/sleonard8_gatech_edu/EdwtfUu37XtGnFbIFONmImIBkd-xXv0NEpZswG5P5-jnJQ?e=AVi8XL


   1. Update the postgres connection in the files utils_generalpy, utils_sql.py and pipeline.py


Note: Currently the database is running on AWS but it will be terminated end of May 2019. The connection details to the database are 
        database="cse6242team22db",
        user="Team22",
        password="vacayaway",
        host="cse6242-db.cvdup1gpakos.us-east-2.rds.amazonaws.com",
        port='5432’


1. TabPy Server Setup:
   1. Download tabpy from https://github.com/tableau/TabPy and unzip the folder to your machine.


   1. Set up a python virtual environment in the folder.
python -m pip install --user virtualenv
python -m venv env
source env/bin/activate


   1. Get requirements.txt and run it in the virtual environment
pip install -r requirements.txt


   1. Copy the files util*.py from the main code folder to the folder env/Libs


   1. Startup the tabpy server using the command startup.cmd in the tabpy server.


   1. Run the Jupyter notebook listingScore.ipynb to deploy the code to the server. This will create the REST endpoint which will run every time the server is run.




1. Tableau workbook:
   1. Import the workbook VacayAway.twbx.
   2. Edit the database connection to point to the postgres database set up.
   3. Download the file neighborhoods.shp and point the Neighborhoods data source to the file.
   4. Go to Help > Manage External Connections and add a Tabpy API server https://localhost:9004


EXECUTION
1. Go to the tabpy folder and run .\startup.sh . This will get the tabpyserver running on the localhost.


1. Run the app:
   1. Go to the tab ‘Dashboard Listings’
   2. Adjust filters
   3. Go to Dashboard -> Run Update on the Menu
   4. Go to Data -> homeaway_v2 + -> Refresh on the Menu


This should give you the updated listings for the filters. To automate the last two steps, the dashboard needs to be published using a Tableau Server which allows automating refreshes. The tabpy can also be hosted on this server.