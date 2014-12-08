import numpy as np
import string

def count_position(stats):
    """ given a dataframe, count the number of each position """
    return np.array(stats.groupby('POS').count()['PLAYER'][['C', 'PF', 'SF', 'SG', 'PG']]) 

def name_to_url(name):
    """ convert a player name to url friendly form """
    return name.lower().replace(' ', '-')

def url_to_name(url):
    """ convert player's url name to formal name """
    if "o'neal" in url:
        return string.capwords(url.replace('-', ' ')).replace('neal', 'Neal')
    elif url == 'darius-johnson-odom':
        return 'Darius Johnson-Odom'
    elif url == 'marshon-brooks':
        return 'MarShon Brooks'
    else:
        return string.capwords(url.replace('-', ' '))
