'''
Authored by Yijun Xiao, Yi Liu

'''
import numpy as np
import pandas as pd
from jinja2 import Environment, PackageLoader
from . import plotting, utility
from salaries_analysis import salaries_stats_analysis
from salaries_analysis import regression

PKG = 'nbastats'
POSITIONS = {'c':'Center', 'pf':'Power Forward', 'sf':'Small Forward', 'sg':'Shooting Guard', 'pg':'Point Guard', 'all' :'All Players'}
STATS = ['PPG', 'RPG', 'APG', 'SPG', 'BPG']
YEARS = xrange(2000, 2015)

def render_leaders(stats, position, n_top, year, temp_dir, temp_file):
    """ take in a dataframe, return rendered templates with data of top player stats in PTS, REB, AST, STL, and BLK """
    leader_stats = []
    plots = []
    for stat in STATS:
        leader_stats.append(stats.sort(stat, ascending=False)[:n_top].to_dict(orient='record'))
        plots.append(plotting.hist_plot(np.array(stats[stat])))
    env = Environment(loader=PackageLoader(PKG, temp_dir))
    template = env.get_template(temp_file)
    return template.render(data=leader_stats, years=YEARS, year=year, season='{}-{}'.format(int(year)-1, year), position=POSITIONS[position], plots=plots)

def render_players(players, position, option, temp_dir, temp_file):
    """ render players_index.html, take in dataframe of players, select players with certain position """
    players_in_pos = np.array(players.PLAYER[players['POS']==position.upper()])
    players_in_pos.sort()
    
    # split into 4 groups for better visualization
    n = len(players_in_pos)
    quarter = int(n/4 + 1)
    players_cols = [players_in_pos[:quarter], players_in_pos[quarter:quarter*2], players_in_pos[quarter*2:quarter*3], players_in_pos[quarter*3:]]

    count = utility.count_position(players)
    env = Environment(loader=PackageLoader(PKG, temp_dir))
    template = env.get_template(temp_file)
    return template.render(option=option, position=position, count=count, players=players_cols)

def render_league_info(counts, temp_dir, temp_file):
    """ plot several charts related to league position counts """
    plots = [plotting.pie_plot(counts[2014]), plotting.pie_plot(counts[2000]), plotting.trend_plot(counts)]
    env = Environment(loader=PackageLoader(PKG, temp_dir))
    template = env.get_template(temp_file)
    return template.render(plots=plots, counts=counts)

def render_player(player, stats, years, year, option, img_src, temp_dir, temp_file):
    """ render page for individual player """
    player_stats = stats.ix[[player]]
    n = len(player_stats)

    # get position, display 3 stats based on position
    pos = player_stats.iloc[0]['POS']
    if pos in set(['PG', 'SG', 'SF']):
        fields = ['PTS', 'AST', 'REB']
        values = player_stats.iloc[0][['PPG', 'APG', 'RPG']]
    else:
        fields = ['PTS', 'REB', 'BLK']
        values = player_stats.iloc[0][['PPG', 'RPG', 'BPG']]
        
    season = str(int(year)-1) + '-' + year[-2:]    # construct season string

    # prepare data for radar chart
    stats = stats[['APG', 'PPG', 'FG%', 'BPG', 'RPG', 'SPG']]
    r_data = (player_stats.iloc[0][['APG', 'PPG', 'FG%', 'BPG', 'RPG', 'SPG']] - stats.min())/(stats.max()-stats.min())
    r_data = np.sqrt(list(r_data))
    fig_name = '{}_{}.png'.format(utility.name_to_url(player), year)
    plotting.radar_plot(r_data, fig_name, pos)
    
    env = Environment(loader=PackageLoader(PKG, temp_dir))
    template = env.get_template(temp_file)
    return template.render(name=player, stats=player_stats, years=years, year=year, option=option, season=season, fields=fields, values=values, rows=xrange(n), fig=fig_name, img_src=img_src)

def render_trend(oa,pos,temp_dir, temp_file):
    """
    render page for salaries trend analysis, including overall trend and trend by positions.
    Attributes:
    oa: an object of overall_analysis class.
    pos: an object of position_analysis class.
    """
    oa_plot, oa_table = oa.overall_salaries_trend() #get overall trend plot and table
    pos_plot = pos.pos_salaries_trend() #get by-position trend plot
    plots = [oa_plot, pos_plot]
    env = Environment(loader=PackageLoader(PKG, temp_dir))
    template = env.get_template(temp_file)
    return template.render(plots=plots, table=oa_table)

def render_distribution(oa,pos,temp_dir, temp_file):
    """
    render page for salaries distribution analysis, including overall distribution and distributions by positions.
    Attributes:
    oa: an object of overall_analysis class.
    pos: an object of position_analysis class.
    """
    oa_plot, oa_table = oa.overall_distributions() #get overall distributions plot and table
    pos_plot, pos_table = pos.pos_salaries_distribution() #get py-position distribution plot and table
    top_10_plot = oa.overall_top_10_player() #get top 10 salaries plot
    dist_table = pd.merge(oa_table, pos_table, left_index=True, right_index=True)
    plots = [oa_plot,pos_plot,top_10_plot]
    env = Environment(loader=PackageLoader(PKG, temp_dir))
    template = env.get_template(temp_file)
    return template.render(plots=plots,table=dist_table,years=xrange(2000,2016),year=oa.year)

def render_regression(sr, temp_dir, temp_file):
    """
    render page for regression analysis.
    Attribute:
    sr: an object of salaries_regression class.
    """
    sr.df = sr.salaries_stats_regression()
    plots = [sr.salaries_stats_regression_plot(),sr.underpriced_player(100),sr.overpriced_player(100)] #get regression analysis plot, underpriced and overpriced plots
    env = Environment(loader=PackageLoader(PKG, temp_dir))
    template = env.get_template(temp_file)
    return template.render(plots=plots,years=xrange(2001,2016),year=sr.year)
    
