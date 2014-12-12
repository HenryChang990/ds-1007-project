
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from salaries_preprocessing import salaries_preprocessing
from salaries_preprocessing import merge_salaries_stats
import mpld3

class salaries_regression(object):
    
    def __init__(self,year=2014):
        self.year = year
        self.df = salaries_preprocessing()
        self.df = merge_salaries_stats(self.df, self.year)
    
    def salaries_stats_regression(self):
        """
        This function is to do linear regression on salaries and nba stats data.
        
        Return:
        self.df: a new dataframe with regression results. 
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
        
        Note:
        By calling this function, you will get a scatter plot on predicted salaries and true salaries.
        """
        
        #self.df[['SALARY','Predicted']].plot(kind='scatter',x='SALARY',y='Predicted',alpha=0.5,color='g',s=50)
        regdata = self.df.reset_index(1)
        regdata = regdata[regdata['POS'].isin(['C','SF','PF','PG','SG'])]
        fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'), figsize=(10,6))
        pos={'C':2,'PF':3,'PG':4,'SF':5,'SG':1}
        posdata = [pos[regdata['POS'][j]] for j in xrange(0,len(regdata.index))]
        scatter = ax.scatter(regdata['SALARY'],
                             regdata['Predicted'], 
                             c=posdata,
                             s=10*regdata['PPG'],
                             color=['skyblue', 'yellowgreen', 'lightcoral', 'mediumpurple','gold'])
        ax.grid(color='white', linestyle='solid')
        labels = [regdata.index[i] for i in xrange(0,len(regdata.index))]
        tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)

        mpld3.plugins.connect(fig, tooltip)
        reference = np.arange(self.df['SALARY'].min(),self.df['SALARY'].max(),1000) 
        #fig = plt.figure()
        plt.plot(reference,reference,'white',alpha=0.7) #a reference line y = x
        plt.title('Regression results for salaries in {}'.format(self.year))
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html
        
    
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
        j=0
        for rect in ax.patches[len(df.index):]:
            ax.text(rect.get_x()+rect.get_width()/2., rect.get_y()+rect.get_height()/4., label+'{percent:.1%}'.format(percent=df['Difference'][i]),ha='center', va='bottom')
            i+=1
        
        for rect2 in ax.patches[:len(df.index)]:
            ax.text(rect2.get_x()+200000, rect2.get_y()+rect2.get_height()/4., '{}'.format(df.index[j]),ha='left', va='bottom',fontsize=14)
            j+=1

    def underpriced_player(self,rank):
        """
        This function is to plot the top 10 underpriced player for a given year in a given range.
        Calling this function, you will get a bar plot.
        
        Attribute:
        rank: a selected ranking range. e.g., if the user wants to see the top 10 overpriced player before ranking 100, then rank = 100
        """
        
        nba_df_SA = self.df[self.df.Predicted > 0] #drop players whose predicted salaries are negtive
        nba_df_SA = nba_df_SA[self.df.RK < rank][['RK','TEAM','SALARY','Predicted','Difference']].reset_index(1) #reset only player as index
        nba_underpriced = nba_df_SA.sort(columns='Difference',ascending=True).head(10).sort(columns='Difference', ascending=False) #select top 10 underpriced players
        nba_underpriced['DIFF'] = nba_df_SA.Predicted - nba_df_SA.SALARY #calculate salaries difference between predicted and true one.
        fig = plt.figure(figsize=(12,6))
        ax = fig.add_subplot(111, axisbg='#EEEEEE')
        ax.grid(color='white', linestyle='solid')
        plt.barh(np.arange(len(nba_underpriced['SALARY'])),
                nba_underpriced['SALARY'],
                height = 0.6,
                color='SkyBlue',
                alpha=0.8)
        plt.barh(np.arange(len(nba_underpriced['SALARY'])),
                nba_underpriced['DIFF'],
                height = 0.6,
                left=nba_underpriced['SALARY'],
                color='grey',
                alpha=0.5)

        #ax = nba_underpriced[['SALARY','DIFF']].plot(kind='barh', stacked=True, alpha=0.5, color = ['g','grey'])
        self.salaries_analysis_add_text(ax,nba_underpriced,'')
        plt.title('Top 10 Underpriced Player in {}'.format(self.year))
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html
    
    def overpriced_player(self,rank):
        """
        This function is to plot the top 10 overpriced player for a given year in a given range.
        Calling this function, you will get a bar plot.
        
        Attributes:
        rank: a selected ranking. e.g., if the user wants to see the top 10 overpriced player before ranking 100, then rank = 100
        """
        
        nba_df_SA = self.df[self.df.Predicted > 0] #drop players whose predicted salaries are negtive
        nba_df_SA = nba_df_SA[self.df.RK < rank][['RK','TEAM','SALARY','Predicted','Difference']].reset_index(1)
        nba_overpriced = nba_df_SA.sort(columns='Difference',ascending=False).head(10).sort(columns='Difference',ascending=True) #select top 10 overpriced players.
        nba_overpriced['DIFF'] = nba_df_SA.SALARY - nba_df_SA.Predicted
        fig = plt.figure(figsize=(12,6))
        ax = fig.add_subplot(111, axisbg='#EEEEEE')
        ax.grid(color='white', linestyle='solid')
        plt.barh(np.arange(len(nba_overpriced['Predicted'])),
                nba_overpriced['Predicted'],
                height=0.6,
                color='SkyBlue',
                alpha=0.8)
        plt.barh(np.arange(len(nba_overpriced['Predicted'])),
                nba_overpriced['DIFF'],
                left=nba_overpriced['Predicted'],
                height = 0.6,
                color='grey',
                alpha=0.5)

        #ax = nba_overpriced[['Predicted','DIFF']].plot(kind='barh', stacked=True, alpha=0.5, color = ['g','grey'])
        self.salaries_analysis_add_text(ax,nba_overpriced,'+')
        plt.title('Top 10 Overpriced Player in {}'.format(self.year))
        html = mpld3.fig_to_html(fig)
        plt.close()
        return html

