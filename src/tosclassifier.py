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
        
    def pull_data(self):
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
        
        return df
    
    def get_data(self):
        '''
        Select data from the dataframe and create our X and y dataframes for our model.
        '''
        full_df = self.create_df()
        full_df = full_df.dropna(axis=0,subset=['quoteText'])
        full_df['label'] = full_df['point']
        full_df.label = full_df.label.replace(['blocker','bad','neutral','good'],[1,1,0,0])
        self.X = full_df.quoteText
        self.y = full_df.label
        
        return self.X,self.y
    
    def vectorize_text(self,X,y,method=TfidfVectorizer,cross_validate=True):
        '''
        Parse and vectorize the text using Term Frequency - Inverse Document Frequency (other methods can be used if preferred).
        Plus an option to not cross_validate date for final production. 
        '''
        X,y = self.get_data()
        if cross_validate:
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X,self.y,test_size=test_size)
            #remove the company names in case of data leakage 
            companies = [company_name.split('.')[0] for company_name in self.get_company_names()]
            tfiddy = TfidfVectorizer(stop_words=companies)
            tfiddy.fit(X_train)
            
    def ensemble_fit(self,X,y,modelnames=['mnb','logreg'],models=
                            [MultinomialNB(alpha=.1),LogisticRegressionCV(solver='lbfgs',Cs=100,max_iter=200)]):
        for name,model in zip(modelnames,models):
            self.name = model
        self.get_data()
        self.mnb.fit(X,y)
        self.logreg.fit(X,y)
        
    def clean_tos(self,new_tos):
        new_tos = new_tos.split('\n')
        new_tos = [term for term in terms_US if term != '']
        self.vectorize_text(cross_validate=False)
        tos_list = []
        for term in new_tos:
            tos_list.append(str(loaded_model.predict(tfidf_model.transform(pd.Series(term)).toarray())))
        
    def predict_proba(self,new_tos):
        new_tos = new_tos.split('\n')
        new_tos = [term for term in terms_US if term != '']
        tos_list = []
        for term in new_tos:
            tos_list.append(str(loaded_model.predict(tfidf_model.transform(pd.Series(term)).toarray())))
        self.mnb.predict_proba(new_tos)
        self.logreg.predict_proba(new_tos)
        
    def get_colors(self,proba,colors=['C7FEDD','DFEEB9','F2DE97','FAA181','F77B7E']):
        self.color_proba = []
        for prob in proba:
            if proba <= 0.2:
                self.color_proba.append(colors[0])
            elif proba > 0.2 and proba <= 0.4:
                self.color_proba.append(colors[1])
            elif proba > 0.4 and proba <= 0.6:
                self.color_proba.append(colors[2])
            elif proba > 0.6 and proba <= 0.8:
                self.color_proba.append(colors[3])
            else:
                self.color_proba.append(colors[4])
        
if __name__ == "__main__":
    tos = ToS_Classifier('../tosdr.org/api/1/service')
    tos.get_data()
    tos.ensemble_fit()
    #pickle and unpickle here
    tos.predict_proba('a string of text divided by spaces')