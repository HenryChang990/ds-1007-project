import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from salaries_preprocessing import salaries_preprocessing
from salaries_preprocessing import salaries_preprocessing_by_year
from salaries_preprocessing import salaries_preprocessing_by_team

class overall_analysis(object):
    
    """
    Overall analysis for salaries
    """
    
    def __init__(self,year):
        self.year = year
        self.df = salaries_preprocessing_by_year()
    
    #Plot overall salaries trend from 2000-2015
    def overall_salaries_trend(self):
        self.df.mean().plot(kind='bar',alpha=0.5,color='g')
        plt.xticks(rotation=-25)
        plt.title('2000-2015 NBA Average Salaries Trend')
        plt.show()
    
    #Plot overall salaries distribution in a given year
    def overall_distributions(self):
        ax = self.df[self.year].hist(bins=30,color='grey',alpha=0.5)
        xmin,xmax,ymin,ymax=ax.axis()
        ax.text(0.8*xmax,0.95*ymax,'Stats Summary in {0}:\n\n{1}'.format(self.year,self.df[self.year].describe()), ha='center', va='top', fontsize=13)
        plt.title('NBA Salaries Distribution in {}'.format(self.year))
        plt.show()
    
    #Plot players with top 10 highest salaries
    def overall_top_10_player(self):
        salaries_top_10 = self.df[self.year].order(ascending=False).head(10).order(ascending=True)
        salaries_top_10 = salaries_top_10.reset_index(1)
        salaries_top_10.plot(kind='barh',legend=False, alpha=0.5)
        plt.title('NBA Top 10 Highest Salaries Players in {}'.format(self.year))
        plt.show()


class position_analysis(object):
    
    def __init__(self,year,pos):
        self.year = year
        self.df = salaries_preprocessing_by_year()
        self.df = self.df.reset_index(1)
        self.pos = pos
    
    #Plot salaries trend for five positions
    def pos_salaries_trend(self):
        salaries_pos_by_year = self.df.groupby('POS').mean().dropna().T
        salaries_pos_by_year.plot(kind='area',color=['dodgerblue','g','crimson','darkviolet','Tan'], linewidth = 1.5, alpha=0.5)
        plt.title('2000-2015 NBA Average Salaries Trend by Positions')
        plt.show()
    
    #Plot salaries distribution for 5 positions in a given year
    def pos_salaries_distribution(self):
        salaries_pos_year = self.df[[self.year,'POS']].dropna()
        salaries_pos_year = salaries_pos_year[salaries_pos_year['POS'].isin(['C','PF','PG','SF','SG'])]
        salaries_pos_year.boxplot(by='POS',sym='r*')
        plt.title('Salaries Distribution by Positions in {}'.format(self.year))
        plt.show()
    
    #Show players with top 10 salaries in a given position at a given year
    def pos_top_10_player(self):
        salaries_pos_year = self.df[[self.year,'POS']].dropna()
        salaries_pos = salaries_pos_year[salaries_pos_year['POS']==self.pos]
        salaries_pos_top_10 = salaries_pos.sort(columns=self.year, ascending=False).head(10).sort(columns=self.year, ascending=True)
        salaries_pos_top_10.plot(kind='barh',legend=False, alpha=0.5)
        plt.title('NBA Top 10 Highest Salaries Center Players in {}'.format(self.year))
        plt.show()


class team_analysis(object):
    
    def __init__(self,team):
        self.team = team
        self.df = salaries_preprocessing_by_team()
    
    
    def team_salaries_trend(self):
        #if pick 1 team, show the salaries trend for this team using bar plot
        self.df[self.team].plot(kind='bar',color='g',alpha=0.5)
        plt.xticks(rotation=-25)
        plt.title('2000-2015 {} Average Salaries Trend'.format(self.team))
        plt.show()
    
    def team_salaries_trend_compare(self):
        
        #if pick many teams, compare salaries trends for selected teams
        self.df[self.team].plot(kind='area',alpha=0.5)
        plt.title('2000-2015 Average Salaries Trend for Selected Teams')
        plt.show()

