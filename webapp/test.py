'''
Authored by Yi Liu, Yijun Xiao

'''
import unittest
import numpy as np
import pandas as pd

from nbastats.salaries_analysis.salaries_preprocessing import salaries_preprocessing, merge_salaries_stats, salaries_preprocessing_by_year
from nbastats.salaries_analysis.salaries_stats_analysis import position_analysis
from nbastats.salaries_analysis.regression import salaries_regression
from nbastats.salaries_analysis.exceptions import cannotLoadDataError
from nbastats.utility import count_position, url_to_name, name_to_url

class data_preprocessing_Test(unittest.TestCase):
    def test_load_data(self):
        salaries = salaries_preprocessing()
        with self.assertRaises(cannotLoadDataError):
            merge_salaries_stats(salaries,1999) #test if it can catch loading data error. There is no 1999 year data in our dataset.

    def test_year(self):
        sy = salaries_preprocessing_by_year()
        years = sy.columns #get columns labels
        self.assertEqual(len(years),len(xrange(2000,2016))) #test if the preprocessed dataframe contains 16 years data
        self.assertIn(2000,years) #check if 2000 data is in the dataframe
        self.assertIn(2015,years) #check if 2015 data is in the dataframe
        self.assertNotIn(1999,years) #check if the dataframe does not contain 1999 data

class data_analysis_pos_Test(unittest.TestCase):
    def test_pos(self):
        pos = position_analysis()
        self.assertIn('POS',pos.df.columns) #check if position information is in the dataframe
        plot, table = pos.pos_salaries_distribution()
        positions = table.columns #get positions information
        self.assertIn('C',positions) #check if positions contain Center
        self.assertIn('PF',positions) #check if positions contain Power Forward
        self.assertNotIn('F',positions) #check if positions do not contain Forward since we respectively consider PF-Power Forward and SF-Small Forward
        self.assertEqual(len(positions),5) #check if it contains 5 positions
        stats = table.index #get distribution stats information
        self.assertIn('mean',stats) #check if mean information is in stats
        self.assertIn('max', stats) #check if max information is in stats
        self.assertIn('std', stats) #check if standard deviation information is in stats

class regression_test(unittest.TestCase):
    def test_reg(self):
        sr = salaries_regression()
        regdata = sr.df.columns
        self.assertIn('SALARY',regdata) #check if salaries data is in the data frame
        self.assertIn('PPG',regdata) #check if stats data, points per game, is in the data frame
        sr.df = sr.salaries_stats_regression()
        regresults = sr.df.columns
        self.assertIn('Predicted',regresults) #check if predicted salaries data is in the regression result dataframe
        self.assertIn('Difference',regresults) #check if salaries' difference ratio data is in the regression result dataframe

class count_position_test(unittest.TestCase):
    def runTest(self):
        stats = pd.DataFrame([dict(PLAYER='Kobe', POS='SG'), dict(PLAYER='T-Mac', POS='SG'),\
                              dict(PLAYER='Yao Ming', POS='C'), dict(PLAYER='Tim Duncan', POS='PF'),\
                              dict(PLAYER='Kevin Garnett', POS='PF'), dict(PLAYER='LeBron', POS='SF'),\
                              dict(PLAYER='Kevin Durant', POS='SF'), dict(PLAYER='Melo', POS='SF'),\
                              dict(PLAYER='Steve Nash', POS='PG')])
        counts = count_position(stats)
        self.assertTrue((counts==np.array([1, 2, 3, 2, 1])).all())

class url_to_name_test(unittest.TestCase):
    def test_normal(self):
        urls = ['steve-nash', 'kobe-bryant', 'yao-ming']
        names = ['Steve Nash', 'Kobe Bryant', 'Yao Ming']
        for i in xrange(len(urls)):
            self.assertEqual(url_to_name(urls[i]), names[i])
            
    def test_dash(self):
        urls = ['darius-johnson-odom', 'al-farouq-aminu']
        names = ['Darius Johnson-Odom', 'Al-Farouq Aminu']
        for i in xrange(len(urls)):
            self.assertEqual(url_to_name(urls[i]), names[i])

    def test_apostrophe(self):
        urls = ["shaq-o'neal", "terry-o'quinn"]
        names = ["Shaq O'Neal", "Terry O'Quinn"]
        for i in xrange(len(urls)):
            self.assertEqual(url_to_name(urls[i]), names[i])

    def test_lebron(self):
        urls = ['lebron-james', 'tracy-mcgrady', 'antonio-mcdyess', 'desagana-diop']
        names = ['LeBron James', 'Tracy McGrady', 'Antonio McDyess', 'DeSagana Diop']
        for i in xrange(len(urls)):
            self.assertEqual(url_to_name(urls[i]), names[i])
            
    def test_iii(self):
        self.assertEqual(url_to_name('john-lucas-iii'), 'John Lucas III')

class name_to_url_test(unittest.TestCase):
    def runTest(self):
        names = ['Steve Nash', 'Al-Farouq Aminu', "Shaq O'Neal", 'Tracy McGrady', 'John Lucas III']
        urls = ['steve-nash', 'al-farouq-aminu', "shaq-o'neal", 'tracy-mcgrady', 'john-lucas-iii']
        for i in xrange(len(urls)):
            self.assertEqual(name_to_url(names[i]), urls[i])
                        
    
if __name__ == '__main__':
    unittest.main()


