acquire.py

###### Imports ######
import pandas as pd
import numpy as np
from env import host, password, user
import os

def get_db_url(db_name, user=user, host=host, password=password):
    """
        This helper function takes as default the user host and password from the env file.
        You must input the database name. It returns the appropriate URL to use in connecting to a database.
    """
    url = f'mysql+pymysql://{user}:{password}@{host}/{db_name}'
    return url

def get_telco_data():
    '''
    This function reads data from the Codeup db into a df. Query is long to customize columns being pulled over.
    '''
    sql_query = """ 
        SELECT 
            customer_id, churn, gender, senior_citizen, partner, dependents,
            tenure, phone_service, multiple_lines,
            online_security, online_backup, device_protection, tech_support,
            streaming_tv, streaming_movies,
            paperless_billing, monthly_charges, total_charges,
      	    it.internet_service_type_id AS 'internet_service_type_id', internet_service_type,
            ct.contract_type_id AS 'contract_type_id', contract_type,
            pt.payment_type_id AS 'payment_type_id', payment_type
        FROM customers AS c
        JOIN internet_service_types AS it ON it.internet_service_type_id = c.`internet_service_type_id`
        JOIN contract_types AS ct ON ct.`contract_type_id` = c.contract_type_id
        JOIN payment_types AS pt ON pt.payment_type_id = c.payment_type_id;
        """
    return pd.read_sql(sql_query, get_db_url('telco_churn'))
    