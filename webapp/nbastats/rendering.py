import numpy as np
from jinja2 import Environment, PackageLoader
from . import plotting, utility

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

def render_player(player, stats, years, img_src, temp_dir, temp_file):
    """ render page for individual player """
    env = Environment(loader=PackageLoader(PKG, temp_dir))
    template = env.get_template(temp_file)
    return template.render(name=player, img_src=img_src)
    
