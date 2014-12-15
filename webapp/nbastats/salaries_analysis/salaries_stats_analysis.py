__author__ = "Yi Liu"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from salaries_preprocessing import salaries_preprocessing
from salaries_preprocessing import salaries_preprocessing_by_year
import mpld3
import os

class overall_analysis(object):
    """
    This is a class for nba salaries overall analysis, it has following functions:
    1) Plot league average salaries trend from 2000-2015.
    2) Analyze salaries distribution in league in each year.
    3) Analyze top 10 salaries players in each year.
    
    Attributes:
    year: a year from 2000 to 2015, int, default=2014.
    df: a preprocessed dataframe with salaries data by year.
    """

    def __init__(self,year=2014):
        """
        Return a overall_analysis object whose year is *year* and df is a preprocessed dataframe.
        """
        self.year = year
        self.df = salaries_preprocessing_by_year()

    def overall_salaries_trend(self):
        """
        This function is to analyze and plot nba salaries trend.

        Return:
        html: a string of html for the salaries trend plot.
        salaries: a dataframe with salaries statistical information (e.g., mean, min, max) in each year. 
        """
        years = xrange(2000,2016)
        salaries = [self.df[year].describe().apply(lambda x: int(x)) for year in years] #store salaries statistical information for each year in a list
        salaries = pd.concat(salaries, axis=1).T.drop(['25%','75%'],1) #merge all salaries statistical information dataframes into a dataframe

        fig = plt.figure(figsize=(10,6))
        ax = fig.add_subplot(111, axisbg='#EEEEEE')
        ax.grid(color='white', linestyle='solid')
        ave_salaries = self.df.mean() #calculate the average salaries for each year
        plt.bar(self.df.columns, ave_salaries, 0.5, color='#0077FF', alpha=0.5)
        ax.set_xlabel('Year', fontsize=16)
        ax.set_ylabel('Average Salaries', fontsize=16)
        ax.xaxis.set_label_coords(0.5,-0.08)
        ax.yaxis.set_label_coords(-0.14,0.5)
        plt.title('2000-2015 NBA Average Salaries Trend')
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html, salaries

    def overall_distributions(self):
        """
        This is a function to analyze and plot NBA salaries distribution.

        Return:
        html: a string of html of the salaries distribution plot.
        overall_dist: a dataframe containing salaries distribution stats.
        """
        overall_dist = pd.DataFrame(self.df[self.year].describe()) #make a dataframe containing salaries statistics information for each year
        overall_dist = overall_dist.rename(columns={self.year: 'League'})
        overall_dist['League'] = overall_dist['League'].apply(lambda x: int(x)) #convert all elements in dataframe to integers
        
        ax = self.df[self.year].hist(bins=30,histtype='stepfilled', fc='#0077FF',alpha=0.5,figsize=(10,6))
        ax.set_axis_bgcolor('#EEEEEE')
        ax.grid(color='white', linestyle='solid')
        ax.set_xlabel('Salaries', fontsize=16)
        ax.xaxis.set_label_coords(0.5,-0.08)
        ax.set_ylabel('Counts', fontsize=16)
        ax.yaxis.set_label_coords(-0.05,0.5)
        fig = ax.get_figure()
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html, overall_dist

    def overall_top_10_player(self):
        """
        This is a function to analyze and plot top 10 salaries players.

        Return:
        html: a string of html of top 10 salaries plot.
        """
        salaries_top_10 = self.df[self.year].order(ascending=False).head(10).order(ascending=True) #get top 10 highest salaries
        salaries_top_10 = salaries_top_10.reset_index(1)
        
        fig = plt.figure(figsize=(10,6))
        ax = fig.add_subplot(111)
        ax.set_axis_bgcolor('#EEEEEE')
        ax.grid(color='white', linestyle='solid')
        plt.barh(np.arange(len(salaries_top_10.index)),
                 salaries_top_10[self.year],
                 height = 0.6,
                 color='SkyBlue',
                 alpha=0.8)

        #add player names into the bar plot
        i = 0
        for rect in ax.patches[:len(salaries_top_10.index)]:
            ax.text(rect.get_x()+200000, 
                    rect.get_y()+rect.get_height()/4., 
                    '{}'.format(salaries_top_10.index[i]),
                    ha='left', 
                    va='bottom',
                    fontsize=14)
            i+=1

        ax.set_xlabel('Salaries', fontsize=16)
        ax.xaxis.set_label_coords(0.5,-0.08)
        ax.set_ylabel('Players', fontsize=16)
        ax.yaxis.set_label_coords(-0.02,0.5)
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html

class position_analysis(object):
    """
    This is a class for salaries analysis by positions. It has following functions:
    1) Analyze and plot salaries trend by positions.
    2) Analyze and plot salaries distribution by positions.

    Attributes:
    year: a year from 2000-2015.
    df: a dataframe to be analyzed.
    """

    def __init__(self,year=2014):
        """
        Return a position_analysis object whose year is *year* and df is a by-year preprocessed dataframe.
        """
        self.year = year
        self.df = salaries_preprocessing_by_year()
        self.df = self.df.reset_index(1)

    def pos_salaries_trend(self):
        """
        This is a function to analyze and plot salaries trend by positions.
        
        Return:
        html: a string of html of by-position salaries trend plot.
        """
        salaries_pos_by_year = self.df.groupby('POS').mean().dropna().T
        
        ax = salaries_pos_by_year.plot(color=['skyblue', 'yellowgreen','gold', 'lightcoral', 'mediumpurple'], linewidth = 2.0, alpha=0.9, figsize=(10,6))
        ax.grid(color='white', linestyle='solid')
        ax.set_axis_bgcolor('#EEEEEE')
        ax.set_xlabel('Year', fontsize=16)
        ax.set_ylabel('Average Salaries', fontsize=16)
        ax.xaxis.set_label_coords(0.5,-0.08)
        ax.yaxis.set_label_coords(-0.14,0.5)
        fig = ax.get_figure()
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html

    def pos_salaries_distribution(self):
        """
        This is a function to analyze and plot salaries distribution by positions.

        Return:
        html: a string of html of by-position salaries distribution plot.
        pos: a dataframe with salaries statistics by positions.
        """
        salaries_pos_year = self.df[[self.year,'POS']].dropna()
        positions = ['C','PF','SF','SG','PG']
        salaries_pos_year = salaries_pos_year[salaries_pos_year['POS'].isin(positions)]
        pos = [salaries_pos_year[salaries_pos_year['POS'] == position].describe().rename(columns={self.year:position}) for position in positions] #store by-position salaries statistics into a list
        pos = pd.concat(pos, axis=1) #merge all by-position dataframes
        #convert all elements in dataframe into integers
        for position in positions:
            pos[position] = pos[position].apply(lambda x: int(x))

        ax = salaries_pos_year.boxplot(by='POS',sym='r*',figsize=(10,6))
        ax.set_axis_bgcolor('#EEEEEE')
        ax.grid(color='white', linestyle='solid')

        #add positions name text into the boxplot
        loc = salaries_pos_year.groupby('POS').median()
        for i in xrange(0,5):
            ax.text(i+1, 
                    loc[self.year][i], 
                    loc.index[i], 
                    ha='center',
                    va='bottom')
        plt.title('')
        ax.set_xlabel('Positions', fontsize=16)
        fig = ax.get_figure()
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html, pos


