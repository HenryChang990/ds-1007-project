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
    elif 'deandre' in url:
        return string.capwords(url.replace('-', ' ')).replace('Deandre', 'DeAndre')
    elif 'marshon' in url:
        return string.capwords(url.replace('-', ' ')).replace('Marshon', 'MarShon')
    elif 'mcgrady' in url:
        return string.capwords(url.replace('-', ' ')).replace('Mcgrady', 'McGrady')
    elif 'dejuan' in url:
        return string.capwords(url.replace('-', ' ')).replace('Dejuan', 'DeJuan')
    elif 'demarcus' in url:
        return string.capwords(url.replace('-', ' ')).replace('Demarcus', 'DeMarcus')
    elif 'lamarcus' in url:
        return string.capwords(url.replace('-', ' ')).replace('Lamarcus', 'LaMarcus')
    elif 'mcroberts' in url:
        return string.capwords(url.replace('-', ' ')).replace('Mcroberts', 'McRoberts')
    elif "o'quinn" in url:
        return string.capwords(url.replace('-', ' ')).replace('quinn', 'Quinn')
    elif "e'twaun" in url:
        return string.capwords(url.replace('-', ' ')).replace('twaun', 'Twaun')
    elif url == 'lebron-james':
        return 'LeBron James'
    elif url == 'demar-derozan':
        return 'DeMar DeRozan'
    elif url == 'john-lucas-iii':
        return 'John Lucas III'
    elif url == 'al-farouq-aminu':
        return 'Al-Farouq Aminu'
    else:
        return string.capwords(url.replace('-', ' '))
