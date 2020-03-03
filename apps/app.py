import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from tosclassifier import ToS_Classifier

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET'])
def index():
    return render_template('classifier.html')

@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    term = user_data['term']
    model = pickle.load(open('classifier.pkl','rb'))
    X,_ = model.get_data()
    probability = model.predict_proba(X,input_user=True,input_X=term)
    classification = model.get_color(probability[:,1])

    results = [
        [{"x": 2, "y": 1},"#C7FEDD"],
        [{"x": 2, "y": 1.5},"#DFEEB9"],
        [{"x": 2, "y": 2},"#F2DE97"],
        [{"x": 2, "y": 2.5},"#C7FEDD"],
        [{"x": 2, "y": 2},"#F2DE97"]]

    for i,color in enumerate(classification):
        results.append([{"x": 5, "y": i},color])

    return jsonify({'results':results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)