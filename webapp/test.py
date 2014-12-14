import unittest
import numpy as np
import pandas as pd
from nbastats.salaries_analysis.salaries_preprocessing import salaries_preprocessing_by_year
from nbastats.salaries_analysis.salaries_stats_analysis import position_analysis
from nbastats.salaries_analysis.regression import salaries_regression

class data_clean_by_year_Test(unittest.TestCase):
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






if __name__ == '__main__':
    unittest.main()


