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
def get_telco_data(sql_query = "SELECT customer_id, monthly_charges, tenure, total_charges FROM customers WHERE `contract_type_id` = 3"):
    '''
    this function takes in a sql query (assign it to a variable) to get data from the  telco_churn database.
    ex (also default query): query = SELECT customer_id, monthly_charges, tenure, total_charges FROM customers
    '''

    return pd.read_sql(sql_query, get_db_url('telco_churn'))\


######################### get generic data #########################
def get_any_data(database, sql_query):
    '''
    put in the query and the database and get the data you need in a dataframe
    '''

    return pd.read_sql(sql_query, get_db_url(database))

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




################ Scaler helper function ################
def my_scaler(train, validate, test, col_names, scaler, scaler_name):
    
    '''
    This function takes in the train validate and test dataframes, columns you want to scale (as a list), a scaler (i.e. MinMaxScaler(), with whatever paramaters you need),
    scaler_name as a string.
    col_names: list of columns to scale
    Scaler_name, should be what you want in the name of your new dataframe columns.
    Adds columns to the train validate and test dataframes. 
    Outputs scaler for doing inverse transforms.
    Ouputs a list of the new column names (what you can use to create the X_train).
    
    example: min_max_scaler, scaled_cols_list = my_scaler(train, validate, test, MinMaxScaler(), 'scaled_min_max')
    
    '''
    
    #create the scaler (input here should be minmax scaler)
    mm_scaler = scaler
    
    # make empty list for return
    scaled_cols_list = []
    
    # loop through columns in col names
    for col in col_names:
        
        #fit and transform to train, add to new column on train df
        train[f'{col}_{scaler_name}'] = mm_scaler.fit_transform(train[[col]]) 
        
        #df['col'].values.reshape(-1, 1)
        
        #transform cols from validate and test (only fit on train)
        validate[f'{col}_{scaler_name}']= mm_scaler.transform(validate[[col]])
        test[f'{col}_{scaler_name}']= mm_scaler.transform(test[[col]])
        
        #add new column name to the list that will get returned
        scaled_cols_list.append(f'{col}_{scaler_name}')
    
    #confirmation print
    print('Your scaled columns have been added to your train validate and test dataframes.')
    
    #returns scaler, and a list of column names that can be used in X_train, X_validate and X_test.
    return scaler, scaled_cols_list   

    







    
#################################### get ZILLOW data ####################################
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



