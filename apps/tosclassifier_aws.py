# the usual imports
import numpy as np
import pandas as pd
import pickle
# nlp imports
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
# model imports
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB,MultinomialNB,ComplementNB
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    
class ToS_Classifier(): 

    def __init__(self,df,stopwords):
        self.df = df
        self.stopwords = stopwords

    def get_data(self):
        '''
        Select data from the dataframe and create our X and y dataframes for our model.
        '''
        self.df = self.df.dropna(axis=0,subset=['quoteText'])
        self.df['label'] = self.df['point']
        self.df.label = self.df.label.replace(['blocker','bad','neutral','good'],[1,1,0,0])
  
        return self.df.quoteText, self.df.label
    
    def vectorize_text(self,X,new_X=None,y=None,cross_validate=False):
        '''
        Parse and vectorize the text using Term Frequency - Inverse Document Frequency (other methods can be used if preferred).
        Plus an option to cross validate for testing with additional y label input. 
        '''
        stopwords = [word.split('.')[0] for word in self.stopwords]
        if cross_validate:
            X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.25)
            #remove the company names in case of data leakage 
            self.tfiddy = TfidfVectorizer(stop_words=stopwords)
            self.tfiddy.fit(X_train)
            return self.tfiddy.transform(X_train).toarray(),self.tfiddy.transform(X_test).toarray(),y_train,y_test
        else:
            self.tfiddy = TfidfVectorizer(stop_words=stopwords)
            self.tfiddy.fit(X)
            if new_X is None:
                return self.tfiddy.fit_transform(X).toarray()
            else:
                return self.tfiddy.transform(new_X).toarray()
            
    def ensemble_fit(self,X_vectorized,y,
                     model_1=MultinomialNB(alpha=.1),model_2=LogisticRegressionCV(solver='lbfgs',Cs=100,max_iter=200)):
        '''
        Ensemble two models
        '''
        self.model_1 = model_1
        self.model_2 = model_2
        self.model_1.fit(X_vectorized,y)
        self.model_2.fit(X_vectorized,y)
        
    def clean_tos(self,X,new_X):
        new_X = new_X.split('\n')
        new_X = [term for term in new_X if term != '']
   
        return self.vectorize_text(X,new_X)
        
    def predict(self,X,test_input=False,test_X=None,input_user=False,input_X=None):
        
        if test_input and test_X is not None:
            self.model_1.predict_proba(test_X)
            self.model_2.predict_proba(test_X)
            return (self.model_1.predict_proba(test_X) + self.model_2.predict_proba(test_X))/2
        if input_user and input_X is not None:
            self.model_1.predict_proba(self.clean_tos(X,input_X))
            self.model_2.predict_proba(self.clean_tos(X,input_X))
            return (self.model_1.predict_proba(self.clean_tos(X,input_X))+
                    self.model_2.predict_proba(self.clean_tos(X,input_X)))/2
        else:
            return 'Set input_test or input_user to True and add the X values to use for prediction.'
        
    def get_colors(self,proba,colors=['#C7FEDD','#DFEEB9','#F2DE97','#FAA181','#F77B7E']):
        self.color_proba = []
        for prob in proba:
            if prob <= 0.2:
                self.color_proba.append(colors[0])
            elif prob > 0.2 and prob <= 0.4:
                self.color_proba.append(colors[1])
            elif prob > 0.4 and prob <= 0.6:
                self.color_proba.append(colors[2])
            elif prob > 0.6 and prob <= 0.8:
                self.color_proba.append(colors[3])
            else:
                self.color_proba.append(colors[4])
        return self.color_proba