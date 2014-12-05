import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from salaries_preprocessing import salaries_preprocessing
from salaries_preprocessing import merge_salaries_stats

class salaries_regression(object):
    
    def __init__(self,year):
        self.year = year
        self.df = salaries_preprocessing()
        self.df = merge_salaries_stats(self.df, self.year)
    
    def salaries_stats_regression(self):
        """
        This function is to do linear regression on salaries and nba stats data.
        
        Attribute:
        nba_df: a merged dataframe with salaries and nba stats for regression.
        
        Return:
        nba_df: a new dataframe with regression results. 
                adding predicted value, and difference between predicted value and true value into original dataframe.
        """
        
        lm = linear_model.LinearRegression() #build linear regression model
        my_lm = lm.fit(self.df.drop(['RK','TEAM','SALARY'],axis=1),self.df['SALARY']) #fit with data
        predict = my_lm.predict(self.df.drop(['RK','TEAM','SALARY'],axis=1)) #get the predicted value
        self.df['Predicted'] = predict #store predicted value into the dataframe
        self.df['Difference'] = (self.df.SALARY - self.df.Predicted)/self.df.Predicted #calculate the difference ratio between predicted value and true value
        return self.df
    
    def salaries_stats_regression_plot(self):
        """
        This function is to plot the regression results.
        
        Attribute:
        nba_df: a dataframe containing regression results.
        
        Note:
        By calling this function, you will get a scatter plot on predicted salaries and true salaries.
        """
        
        self.df[['SALARY','Predicted']].plot(kind='scatter',x='SALARY',y='Predicted',alpha=0.5,color='g',s=50)
        reference = np.arange(self.df['SALARY'].min(),self.df['SALARY'].max(),1000) 
        plt.plot(reference,reference,'k--',alpha=0.7) #a reference line y = x
        plt.show()
    
    def salaries_analysis_add_text(self,ax,df,label):
        """
        This function is to add text on salaries regression plot.
        The added text is the difference ratio between predicted salaries and true salaries.
        *ratio = (true salaries - predicted salaries)/predicted salaries*
        
        Attributes:
        ax: a plot to add text
        df: a dataframe with predicted and true salaries data
        label: if is overpriced, '+'; if is underpriced, ''.
        """
        
        i=0
        for rect in ax.patches[len(df.index):]:
            ax.text(rect.get_x()+rect.get_width()/2., rect.get_y()+rect.get_height()/4., label+'{percent:.1%}'.format(percent=df['Difference'][i]),ha='center', va='bottom')
            i+=1
    
    def underpriced_player(self,rank):
        """
        This function is to plot the top 10 underpriced player for a given year in a given range.
        Calling this function, you will get a bar plot.
        
        Attributes:
        nba_df: a dataframe containing regression results.
        year: a year from 1999-2014.
        """
        
        nba_df_SA = self.df[self.df.Predicted > 0] #drop players whose predicted salaries are negtive
        nba_df_SA = nba_df_SA[self.df.RK < rank][['RK','TEAM','SALARY','Predicted','Difference']].reset_index(1) #reset only player as index
        nba_underpriced = nba_df_SA.sort(columns='Difference',ascending=True).head(10).sort(columns='Difference', ascending=False) #select top 10 underpriced players
        nba_underpriced['DIFF'] = nba_df_SA.Predicted - nba_df_SA.SALARY #calculate salaries difference between predicted and true one.
        ax = nba_underpriced[['SALARY','DIFF']].plot(kind='barh', stacked=True, alpha=0.5, color = ['g','grey'])
        self.salaries_analysis_add_text(ax,nba_underpriced,'')
        plt.title('Top 10 Underpriced Player in {}'.format(self.year))
        plt.show()
    
    def overpriced_player(self,rank):
        """
        This function is to plot the top 10 overpriced player for a given year in a given range.
        Calling this function, you will get a bar plot.
        
        Attributes:
        nba_df: a dataframe containing regression results.
        rank: a selected ranking. e.g., if the user wants to see the top 10 overpriced player before ranking 100, then rank = 100
        year: a year from 1999-2014.
        """
        
        nba_df_SA = self.df[self.df.Predicted > 0] #drop players whose predicted salaries are negtive
        nba_df_SA = nba_df_SA[self.df.RK < rank][['RK','TEAM','SALARY','Predicted','Difference']].reset_index(1)
        nba_overpriced = nba_df_SA.sort(columns='Difference',ascending=False).head(10).sort(columns='Difference',ascending=True) #select top 10 overpriced players.
        nba_overpriced['DIFF'] = nba_df_SA.SALARY - nba_df_SA.Predicted
        ax = nba_overpriced[['Predicted','DIFF']].plot(kind='barh', stacked=True, alpha=0.5, color = ['g','grey'])
        self.salaries_analysis_add_text(ax,nba_overpriced,'+')
        plt.title('Top 10 Overpriced Player in {}'.format(self.year))
        plt.show()
