import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations

############################## months to years ##############################

def months_to_years(df, col_with_months = 'tenure'):
    '''
    This function takes in a dataframe and a column you want to change from months to years. Default column is tenure
    Bins for years are 0-11 = 0, 12-23 = 1, 24-35= 2, ...
    '''
    
    df['tenure_years'] = df[col_with_months] // 12
    
    return df


############################## plotting variable pairs for continous vars ############################# 

# TODOAdd plot titles

def plot_variable_pairs(df, cont_vars, dot_color = 'tab:blue', line_color = 'orange'):
    '''
    df = dataframe you want to pull from
    cont_vars = list of names of continuous variables for plotting
    dot_color = what color you want the dots to be (string), default is tableau blue
    line_color = what color you want the reg line to be (string), default is orange
    This function takes in a dataframe and a list of continous variables
    Plots them pairwise (only one plot for each relationship), with a regression line on a scatter plot
    '''
    # get combinations of all variables in list
    combos = combinations(cont_vars,2)
    
    # loop through iterables aka looping through the unique pairs of variables
    for combo in combos:
        
        # unpack each tuple
        x, y = combo
        
        # plot each one using the data from the inputted dataframe. use dot color and line color
        sns.regplot(x = x, y = y, data=df, scatter_kws = {'color': dot_color}, line_kws = {'color': line_color})
        plt.show()



############################## plot the cat and continous variables ##############################

def plot_cat_and_cont(df, cat_vars, cont_vars):
    '''
    df = dataframe you're graphing
    This function takes in a list of categorical variables and continous variable and plots a swarm plot, box plot, and violin plot for each pair
    '''
    # multiply length of continuous variables and length of categorical variables. This is the amount of rows in subplot, and helps set figsize to be tall enough
    num_graphs = len(cont_vars) * len(cat_vars)
    
    # set up figure and axes subplot stuff. Figsize height will adjust to number of rows there should be
    fig, axes = plt.subplots(num_graphs, 3, figsize = (20 , (num_graphs * 5)), squeeze = False)
    
    #initalize my row counter
    row = 0
    
    # loop through continouse variables
    for cont in cont_vars:
        
        # inner loop through categorical variables
        for cat in cat_vars:
            
            # plot all three plots (can change which ones you would like to use here)
            # [row] is the row number we're on, [0] is left most graph in subplot
            sns.swarmplot(x=cat, y=cont, data=df, ax = axes[row][0])
            axes[row][0].set_title(f'{cat} and {cont}')
            
            sns.boxplot(x=cat, y=cont, data=df, ax = axes[row][1])
            axes[row][1].set_title(f'{cat} and {cont}')
            
            sns.violinplot(x = cat, y = cont, data =df, ax = axes[row][2])
            axes[row][2].set_title(f'{cat} and {cont}')
        
            # add one to row to move to next row for the next round
            row = row + 1
            
            # loading check can take out this line
            print(f'Working ---- {row}')
    # show it all
    plt.show()