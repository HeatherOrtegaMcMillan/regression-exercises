# Wrangling functions


################ Imports ################
import pandas as pd
import numpy as np
from env import host, password, user
import os

from sklearn.model_selection import train_test_split

###################### Getting database Url ################
def get_db_url(db_name, user=user, host=host, password=password):
    """
        This helper function takes as default the user host and password from the env file.
        You must input the database name. It returns the appropriate URL to use in connecting to a database.
    """
    url = f'mysql+pymysql://{user}:{password}@{host}/{db_name}'
    return url


################ Getting appropriate telco data ################
def get_telco_data(sql_query = "SELECT customer_id, monthly_charges, tenure, total_charges FROM customers"):
    '''
    this function takes in a sql query (assign it to a variable) to get data from the  telco_churn database.
    ex (also default query): query = SELECT customer_id, monthly_charges, tenure, total_charges FROM customers
    '''

    return pd.read_sql(sql_query, get_db_url('telco_churn'))

################ train test split helper function ################
def banana_split(df):
    '''
    args: df
    This function take in the telco_churn data data acquired by aquire.py, get_telco_data(),
    performs a split.
    Returns train, validate, and test dfs.
    '''
    train_validate, test = train_test_split(df, test_size=.2, 
                                        random_state=713)
    train, validate = train_test_split(train_validate, test_size=.3, 
                                   random_state=713)
    print(f'train --> {train.shape}')
    print(f'validate --> {validate.shape}')
    print(f'test --> {test.shape}')
    return train, validate, test

################ wrangle telco data ################
def wrangle_telco():
    # get dataframe using get_telco_data function
    df = get_telco_data()
    # deal with space values (turn to 0s)
    df['total_charges'] = df['total_charges'].str.replace(' ', '0').astype('float')
    return df

    
################## get zillow data ##################
def get_zillow_data():
    '''
    This function reads in Zillow data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    sql_query = ''' SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    FROM properties_2017
    WHERE propertylandusetypeid = 261;
    '''
    if os.path.isfile('zillow_data.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('zillow_data.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = pd.read_sql(sql_query, get_db_url('zillow'))
        
        # Cache data
        df.to_csv('zillow_data.csv')

    return df


def handle_NaNs(df):
    '''
    This function handles the NaN values for the Zillow data (could be used for other dataframes). 
    Takes in a dataframe and returns a dataframe with the unneeded rows dropped.
    '''
    # drop the duplicated rows
    df = df.drop_duplicates(keep = 'first')
    
    # drop any rows that have NaN values
    df = df.drop(df[df.isna().any(axis=1)].index)
    
    return df


def wrangle_zillow():
    '''
    This function handels getting the data from the zillow database and getting rid of the unneeded rows.
    It returns the dataframe ready to work with.
    Uses other helper functions in wrangle.py to get this done. 
    '''

    df = get_zillow_data()

    df = handle_NaNs(df)

    return df