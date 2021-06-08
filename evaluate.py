import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

################################################################################################
def sse_compare(sse1, sse2, model1, model2 = 'baseline'):
    '''
    sse1 must be for model 1
    sse2, must be for model 2 (which is by default the baseline)
    model1 = string name of the model you're comparing
    This function compares two SSEs. and outputs which one performed better
    '''
    
    if sse1 > sse2:
        print(f'{model1} is not better than {model2}.')
    elif sse1 < sse2:
        print(f'{model1} is better than {model2}. Difference: {sse2 - sse1:.2f}')
    else:
        print(f'{model1} performs the same as {model2}')

################################################################################################
def plot_residuals(df, x_list, palette = "tab10"):
    '''
    This function takes in a dataframe and a list of all the risiduals you would like to plot (that means the names of the columns)
    '''
    color_list= list(sns.color_palette(palette))
    fig, ax = plt.subplots(figsize=(10, 5))
    for x, c in zip(x_list, color_list):
        sns.histplot(x = x, data = df, kde=True, ax = ax, alpha = 0.5, color = c, legend=True, lw = .1)
    
    plt.legend(x_list)  
    plt.show()

################################################################################################

def hip_to_be_square(y, yhat, print_out = False):
    '''
    This function takes the actuals (y), 
    and the predictions (yhat).
    optional arguement print_out. bool. when set to True will print out summary
    It prints out the Sum of SE, Mean SE, Root Mean SE, Explained SS, and Total SS. 
    Returns them in 5 variables. In order listed above
    ex: sse, mse, rmse, ess, tss = hip_to_be_square(df, 'actuals', 'yhat', print_out = True)
    '''
    # calculate Sum of Squared Error
    sse = ((y - yhat) ** 2).sum()
    
    # calculate Mean of Squared Error
    mse = sse / y.shape[0]
    
    # calculate Root Mean of Squared Error
    rmse = mse ** .5
    
    # calculate Explained Sum of Squares 
    ess = ((yhat - y.mean()) ** 2).sum()
    
    # calculate Total Sum of Squares
    tss = ((y - y.mean()) ** 2).sum()
    
    if print_out == True:
        
        print(f'''
            The Sum of Squared Error: {sse:.2f}
            The Mean Squared Error: {mse:.2f}
            The Root Mean Squared error: {rmse:.2f}
            -----------------------------------
            The Mean Explained Sum of Squares: {ess:.2f}
            The Total Sum of Squares: {tss:.2f}
            ''')
    return sse, mse, rmse, ess, tss

################################################################################################
def baseline_mean_errors(y):
    '''
    This function takes in the actuals (y). Computes the baseline model. 
    Returns the SSE, MSE, and RMSE for the baseline
    '''
    baseline = y.mean()
    
    # calculate Sum of Squared Error
    sse = ((y - baseline) ** 2).sum()
    
    # calculate Mean of Squared Error
    mse = sse / y.shape[0]
    
    # calculate Root Mean of Squared Error
    rmse = mse ** .5
    
    return sse, mse, rmse

################################################################################################

def better_than_baseline(y, yhat):
    '''
    This function takes in actuals (y) and predictions (yhat) 
    and returns true if the model performs better than baseline. 
    '''
    # calculate values for baseline
    sse_b, mse_b, rmse_b = baseline_mean_errors(y)
    
    # calculate values for model
    sse, mse, rmse_model, ess, tss = hip_to_be_square(y, yhat, print_out=False)
    
    # compare rmse from baseline and model
    
    # If Root Mean Square Error is smaller for the model than for the baseline, model is better, return True
    if rmse_model < rmse_b:
        return True
    # if Root mean Square error for the model is larger or the same as the baseline, return False 
    else:
        return False