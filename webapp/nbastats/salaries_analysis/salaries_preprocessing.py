__author__="Yi Liu"

import numpy as np
import pandas as pd
import os
from exceptions import cannotLoadDataError

def salaries_preprocessing():
    """
    This function is to preprocess 2000 - 2015 salaries dataset.
    Return: a merged dataset containing 2000-2015 salaries data.
    """
    s_year = xrange(2000, 2016)
    #load 2000-2015 salaries data into a dictionary
    try:
        dfs = {year:pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"/../static/data/salaries_"+str(year)+".csv").dropna(subset = ['SALARY']) for year in s_year}
    except:
        raise cannotLoadDataError('Salaries Data Not Found!')
    for year in s_year:
        dfs[year]['POS'].fillna('N', inplace=True)
        dfs[year] = dfs[year].set_index(['PLAYER','POS'])
    return pd.concat(dfs, axis=1, join='outer') #merge 2000-2015 dataframes into a dataframe


def salaries_preprocessing_by_year():
    """
    This function is to prepocess salaries dataset by year
    Return:
    salaries_by_year: a dataframe containing every year's salaries for each player from 2000 to 2015
    """
    df = salaries_preprocessing()
    df.columns = df.columns.get_level_values(1)
    salaries_by_year = df['SALARY']
    salaries_by_year.columns=xrange(2000,2016) #rename columns names with years
    return salaries_by_year


def merge_salaries_stats(salaries, year):
    """
    This function is to merge salaries dataset and nba stats dataset for a given year.
    Since this function is called for preparing for the regression analysis and we are trying regress next year's salaries on this year's statistics, therefore,
    *statistics year = salaries year - 1*
    
    Attributes:
    salaries: a preprocessed salaries dataset
    year: a salaries year, from 2000 to 2015
    
    Return:
    a merged dataframe with salaries and nba stats dataset for the selected year.
    """
    try:
        salaries_year = salaries[year].dropna(subset = ['SALARY'])
        stats_year = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+'/../static/data/stats_{}.csv'.format(year-1)) #load stats data
    except:
        raise cannotLoadDataError('NBA Stats Data Not Found!')
    stats_year = stats_year[stats_year['POS'].isin(['C','PF','PG','SF','SG'])] #check positions 
    stats_year = stats_year.sort(columns='PLAYER')
    stats_year = stats_year.drop_duplicates(subset=['PLAYER','POS'])
    stats_year = stats_year.set_index(['PLAYER','POS'])
    stats_year = stats_year.drop('TEAM',1)
    return pd.merge(salaries_year,stats_year,right_index=True, left_index=True)


