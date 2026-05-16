import pandas as pd
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import logging
import time

logging.basicConfig(
    filename = 'logs/ingestion_db.log',
    level = logging.DEBUG,
    format =  "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)

# Step 1: Connect to PostgreSQL
# Replace placeholders with your actual details
username = "postgres"      # default user
password = quote_plus("Pr@tik2001") # the password you set during installation
host = "localhost"         # if running locally
port = "5432"              # default PostgreSQL port
database = "vendors_data"    # the database you created in pgAdmin

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# If your data comes from a server every 10min then you need to 
# write a script that runs automatically for every 10 min and ingest that data to the database.
def ingest_db(df,table_name,engine):
    df.to_sql(table_name, con = engine, if_exists="replace", index=False, chunksize=10000, method='multi')

def load_raw_data():
    '''This function will load csv as dataframe and ingest into the database'''
    start = time.time()
    for file in os.listdir('C:/Users/hp/OneDrive/Desktop/Data_Analytics_Course/Data_Analysis/0_Resources/Vendors Data'):
        if '.csv' in file:
            df=pd.read_csv('C:/Users/hp/OneDrive/Desktop/Data_Analytics_Course/Data_Analysis/0_Resources/Vendors Data/'+file)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df,file[:-4],engine)
    end = time.time()
    total_time = (end - start)/60
    logging.info('--------Ingestion Complete--------')
    logging.info(f'\nTotal time taken : {total_time} minutes')

if __name__ == '__main__':
    load_raw_data()