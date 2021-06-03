
################ Imports ################
import pandas as pd
import numpy as np
from env import host, password, user
import os


###################### Getting database Url ################
def get_db_url(db_name, user=user, host=host, password=password):
    """
        This helper function takes as default the user host and password from the env file.
        You must input the database name. It returns the appropriate URL to use in connecting to a database.
    """
    url = f'mysql+pymysql://{user}:{password}@{host}/{db_name}'
    return url


################ Getting appropriate telco data ################
def get_telco_data(sql_query):
    '''
    this function takes in a sql query (assign it to a variable) to get data from the  telco_churn database.
    ex: query = query = SELECT customer_id, monthly_charges, tenure, total_charges FROM customers
    '''
    return pd.read_sql(sql_query, get_db_url('telco_churn'))
    