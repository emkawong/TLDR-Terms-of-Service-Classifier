# the usual imports
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
# create a list of file names to pull each json file
from os import listdir
from os.path import isfile, join
# get JSON files from TOS API
import string
import urllib, json
# nlp imports
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
# model imports
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB,MultinomialNB,ComplementNB
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
# metric imports
from sklearn.metrics import roc_curve, auc
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize

class ToS_Classifier():

    def __init__(self,directory):
        self.directory = directory

    def get_company_names(self):
        '''
        After cloning the TOS;DR data - point into their main directory to get list of terms by company, 
        remove companies with non-ASCII characters (plus manually removing companies with mostly non-ASCII reviews).
        '''
        company_names = [f for f in listdir(self.directory) if isfile(join(self.directory, f))]
        ascii_chars = set(string.printable)
        nonenglish = {word for word in company_names for letter in word if letter not in ascii_chars}
        nonenglish.remove( 'coinbase–.json')
        return [company for company in company_names if company not in nonenglish]
        
    def get_data(self):
        '''
        Get data for each company.
        '''
        companies = self.get_company_names()
        data = []
        for company in companies:
            with open(f'{self.directory}/{company}') as json_data:
                data.append(json.load(json_data))
        return data

    def create_df(self):
        '''
        From the converted data, create dataframes containing all pertinent information.
        '''
        all_data = self.get_data()
        pd_list = []
        for data in all_data:
            pd_list.append(pd.DataFrame.from_dict(data['pointsData']).T)
            
        alldata_df = pd.concat(pd_list,axis=0).reset_index()
        alldata_df = alldata_df.loc[:,['id','quoteText','services','title','tosdr']]
        todsr_df = pd.json_normalize(alldata_df['tosdr'])
        df = pd.concat((alldata_df,todsr_df),axis=1)
        df = df.drop('tosdr',axis=1).explode('services')
        self.df = df

        return df

if __name__ == "__main__":
    tos = ToS_Classifier('tosdr.org/api/1/service')
    tos.create_df()