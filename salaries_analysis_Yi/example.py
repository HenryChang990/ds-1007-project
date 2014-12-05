import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from salaries_analysis.regression import *
from salaries_analysis.salaries_stats_analysis import *

def example():
    """
    An example to show the salaries analysis results.
    Example:
    year: 2014
    position: C--Center
    Team: Boston
    """
    
    print "========Welcome to NBA Salaries Analysis for 2014========"
    #Results of salaries regression
    sr = salaries_regression(2014)
    sr.df = sr.salaries_stats_regression() #merge the salaries and stats df
    print "Showing the salaries vs. NBA stats regression plot......"
    sr.salaries_stats_regression_plot() #plot regression results
    print "Showing the top 10 overpriced players......"
    sr.overpriced_player(100) #plot overpriced player from players with top 100 salaries
    print "Showing the top 10 Underpriced players......"
    sr.underpriced_player(100) #plot underpriced player from players with top 100 salaries

    #Results for overall analysis
    oa = overall_analysis(2014)
    print "Showing the overall salaries trend from 2000-2015......."
    oa.overall_salaries_trend()
    print "Showing the overall salaries distribution in 2014......"
    oa.overall_distributions()
    print "Showing players with top 10 salaries in 2014......"
    oa.overall_top_10_player()
    
    #Results for position analysis
    pos = position_analysis(2014,'C')
    print "Showing the salaries trend by positions......"
    pos.pos_salaries_trend()
    print "Showing the salaries distribution in 2014 by positions......"
    pos.pos_salaries_distribution()
    print "Showing the center players with top 10 salaries in 2014......"
    pos.pos_top_10_player()
    
    #Results for team analysis
    team = team_analysis('Boston Celtics')
    print "Showing the salaries trend for Boston Celtics......"
    team.team_salaries_trend()
    teams = team_analysis(['Atlanta Hawks','Boston Celtics','Philadelphia 76ers','Brooklyn Nets'])
    print "Showing the salaries trend for selected teams......"
    teams.team_salaries_trend_compare()
    
    print "=============Thank you! Bye!=============="    

def main():
    example()


if __name__ == '__main__':
    main()
