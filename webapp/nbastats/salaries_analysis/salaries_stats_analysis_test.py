
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from salaries_preprocessing import salaries_preprocessing
from salaries_preprocessing import salaries_preprocessing_by_year
from salaries_preprocessing import salaries_preprocessing_by_team
import mpld3
import os

class overall_analysis(object):


    """
    Overall analysis for salaries
    """

    def __init__(self,year=2014):
        self.year = year
        self.df = salaries_preprocessing_by_year()

    #Plot overall salaries trend from 2000-2015
    def overall_salaries_trend(self):
        years = xrange(2000,2016)
        salaries = [self.df[year].describe().apply(lambda x: int(x)) for year in years]
        salaries = pd.concat(salaries, axis=1).T.drop(['25%','75%'],1)

        fig = plt.figure(figsize=(10,6))
        ax = fig.add_subplot(111, axisbg='#EEEEEE')
        ax.grid(color='white', linestyle='solid')
        ave_salaries = self.df.mean() #calculate the average salaries for each year
        #width = 0.5
        plt.bar(self.df.columns, ave_salaries, 0.5, color='#0077FF', alpha=0.5)

        #plt.xticks(self.df.columns+width/2.)
        plt.title('2000-2015 NBA Average Salaries Trend')
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html, salaries

    #Plot overall salaries distribution in a given year
    def overall_distributions(self):
        overall_dist = pd.DataFrame(self.df[self.year].describe()) #make a dataframe containing salaries statistics information for each year
        overall_dist = overall_dist.rename(columns={self.year: 'League'})
        overall_dist.League = overall_dist.League.apply(lambda x: int(x)) #convert all elements in dataframe to integers
        ax = self.df[self.year].hist(bins=30,histtype='stepfilled', fc='#0077FF',alpha=0.5,figsize=(10,6))
        ax.set_axis_bgcolor('#EEEEEE')
        ax.grid(color='white', linestyle='solid')
        #xmin,xmax,ymin,ymax=ax.axis()
        #ax.text(0.8*xmax,0.95*ymax,'Stats Summary in {0}:\n\n{1}'.format(self.year,self.df[self.year].describe()), ha='center', va='top', fontsize=13)
        plt.title('NBA Salaries Distribution in {}'.format(self.year))
        fig = ax.get_figure()
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html, overall_dist


    #Plot players with top 10 highest salaries
    def overall_top_10_player(self):
        salaries_top_10 = self.df[self.year].order(ascending=False).head(10).order(ascending=True) #get top 10 highest salaries
        salaries_top_10 = salaries_top_10.reset_index(1)
        fig = plt.figure(figsize=(12,6))
        ax = fig.add_subplot(111)
        ax.set_axis_bgcolor('#EEEEEE')
        ax.grid(color='white', linestyle='solid')
        plt.barh(np.arange(len(salaries_top_10.index)),
                 salaries_top_10[self.year],
                 height = 0.6,
                 color='SkyBlue',
                 alpha=0.8)

        i = 0
        for rect in ax.patches[:len(salaries_top_10.index)]:
            ax.text(rect.get_x()+200000, 
                    rect.get_y()+rect.get_height()/4., 
                    '{}'.format(salaries_top_10.index[i]),
                    ha='left', 
                    va='bottom',
                    fontsize=14)
            i+=1

        #ax = salaries_top_10.plot(kind='barh',legend=False, alpha=0.5,figsize=(10,6))
        #ax.set_axis_bgcolor('#EEEEEE')
        plt.title('NBA Top 10 Highest Salaries Players in {}'.format(self.year))
        #fig = ax.get_figure()
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html
        #return salaries_top_10

class position_analysis(object):

    def __init__(self,year=2014,pos='C'):
        self.year = year
        self.df = salaries_preprocessing_by_year()
        self.df = self.df.reset_index(1)
        self.pos = pos

    #Plot salaries trend for five positions
    def pos_salaries_trend(self):
        salaries_pos_by_year = self.df.groupby('POS').mean().dropna().T
        ax = salaries_pos_by_year.plot(color=['skyblue', 'yellowgreen','gold', 'lightcoral', 'mediumpurple'], linewidth = 2.0, alpha=0.9, figsize=(10,6))
        ax.grid(color='white', linestyle='solid')
        ax.set_axis_bgcolor('#EEEEEE')
        plt.title('2000-2015 NBA Average Salaries Trend by Positions')
        fig = ax.get_figure()
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html

    #Plot salaries distribution for 5 positions in a given year
    def pos_salaries_distribution(self):
        salaries_pos_year = self.df[[self.year,'POS']].dropna()
        positions = ['C','PF','SF','SG','PG']
        salaries_pos_year = salaries_pos_year[salaries_pos_year['POS'].isin(positions)]
        pos = [salaries_pos_year[salaries_pos_year['POS'] == position].describe().rename(columns={self.year:position}) for position in positions]
        pos = pd.concat(pos, axis=1)
        for position in positions:
            pos[position] = pos[position].apply(lambda x: int(x))

        ax = salaries_pos_year.boxplot(by='POS',sym='r*',figsize=(10,6))
        ax.set_axis_bgcolor('#EEEEEE')
        ax.grid(color='white', linestyle='solid')
        loc = salaries_pos_year.groupby('POS').median()
        for i in xrange(0,5):
            ax.text(i+1, 
                    loc[self.year][i], 
                    loc.index[i], 
                    ha='center',
                    va='bottom')
        plt.title('Salaries Distribution by Positions in {}'.format(self.year))
        fig = ax.get_figure()
        #plt.savefig(os.path.join(os.path.dirname(__file__), '../static/img/pos_dist_{}.png'.format(self.year)), bbox_inches='tight')
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html, pos


