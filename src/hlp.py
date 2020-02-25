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

def gather_data(directory):
    
    '''
    After cloning the TOS;DR data - point into their main directory to get list of terms by company, 
    remove companies with non-ASCII characters (plus manually removing companies with mostly non-ASCII reviews), 
    and gather data by company.
    '''
    companies = [f for f in listdir(directory) if isfile(join(directory, f))]
    ascii_chars = set(string.printable)
    nonenglish = {word for word in companies for letter in word if letter not in ascii_chars}
    nonenglish.remove( 'coinbase–.json')
    english_co = [company for company in companies if company not in nonenglish]
    
    data_list = []
    for company in english_co:
        with open(f'{directory}/{company}') as json_data:
            data_list.append(json.load(json_data))
            
    return english_co,data_list

def create_df(data):

    '''
    From the converted data, create dataframes containing all pertinent information.
    '''

    pd_list = []
    for data in data:
        pd_list.append(pd.DataFrame.from_dict(data['pointsData']).T)
        
    alldata_df = pd.concat(pd_list,axis=0).reset_index()
    alldata_df = alldata_df.loc[:,['id','quoteText','services','title','tosdr']]
    todsr_df = pd.json_normalize(alldata_df['tosdr'])
    df = pd.concat((alldata_df,todsr_df),axis=1)
    df = df.drop('tosdr',axis=1).explode('services')
    
    return df
    