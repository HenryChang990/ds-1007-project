import numpy as np

def count_position(stats):
    """ given a dataframe, count the number of each position """
    return np.array(stats.groupby('POS').count()['PLAYER'][['C', 'PF', 'SF', 'SG', 'PG']]) 
